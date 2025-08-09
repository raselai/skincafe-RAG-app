import streamlit as st
from openai import OpenAI
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
import json
import re
import requests
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

def display_product_image(image_url):
    """Display a product image in the Streamlit UI."""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Product Image", use_column_width=True)
        else:
            st.error(f"Failed to load image from {image_url}")
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")

def extract_image_urls(text):
    """Extract image URLs from text."""
    # Look for URLs in the text
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = re.findall(url_pattern, text)
    
    # Filter for image URLs
    image_urls = [url for url in urls if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))]
    return image_urls

# Function to initialize the RAG components
@st.cache_resource
def initialize_rag():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Use JSONLoader for SkinCafe products
    loader = JSONLoader(
        file_path="data/skincafe_products.json",
        jq_schema='.[]',  # This extracts each item in the top-level array
        text_content=False
    )
    documents = loader.load()
    
    # No need for text splitting if each JSON object is already a suitable size
    # If splitting is still needed, uncomment the following lines:
    # text_split = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    # documents = text_split.split_documents(documents)
    
    db = FAISS.from_documents(documents, OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")))
    
    llm = ChatOpenAI(model_name="gpt-4.1-nano", api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI assistant for SkinCafe, a premium cosmetics e-commerce platform. Your job is to help customers find the perfect skincare and beauty products that match their needs.

        SkinCafe offers a wide range of high-quality cosmetics including:
        - Skincare products (cleansers, toners, serums, moisturizers)
        - Hair care products (shampoos, conditioners, treatments)
        - Body care products (lotions, oils, scrubs)
        - Essential oils and natural products
        
        Your task is to:
        1. Understand the customer's skin type, concerns, and preferences
        2. Recommend appropriate products from SkinCafe's catalog
        3. Provide detailed information about product benefits and ingredients
        4. Include product images and prices in your recommendations
        5. Ask follow-up questions to better understand customer needs
        6. Guide customers to make informed purchasing decisions
        
        When recommending products:
        - Always include the product image URL
        - Mention the current price (regular or sale price)
        - Ask if the customer wants to know more details or visit the product page
        - Consider the customer's budget and preferences
        - Suggest complementary products when relevant
        
        Context:
        <context>
        {context}
        </context>
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    history_aware_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
    ])
    
    retriever = db.as_retriever()
    history_aware_retriever = create_history_aware_retriever(llm, retriever, history_aware_prompt)
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain

# Streamlit UI
st.title("SkinCafe AI Beauty Assistant")

# Add clickable logo
st.markdown(
    """
    <div style="background-color: white; padding: 10px; display: inline-block; border-radius: 5px;">
        <a href="https://skincafe.co/">
            <img src="https://skincafe.co/wp-content/uploads/2023/12/imageedit_2_2841019257.png" width="200">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize RAG components
rag_chain = initialize_rag()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If it's an assistant message, check for and display images
        if message["role"] == "assistant":
            image_urls = extract_image_urls(message["content"])
            for url in image_urls:
                display_product_image(url)

# User input
user_input = st.chat_input("Ask about our beauty products...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Convert chat history to the format expected by the RAG chain
        rag_history = [
            HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"])
            for msg in st.session_state.chat_history[:-1]  # Exclude the latest user message
        ]
        
        # Generate response
        ai_response = rag_chain.invoke({"input": user_input, "chat_history": rag_history})
        full_response = ai_response["answer"]
        
        message_placeholder.markdown(full_response)
        
        # Display any images in the response
        image_urls = extract_image_urls(full_response)
        for url in image_urls:
            display_product_image(url)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
