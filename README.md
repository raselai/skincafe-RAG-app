# SkinCafe AI Beauty Assistant

An intelligent AI-powered beauty product recommendation system for SkinCafe cosmetics e-commerce platform. This application uses Retrieval-Augmented Generation (RAG) technology to help customers find the perfect skincare and beauty products through natural language conversations.

## Demo Video

Watch the SkinCafe AI Beauty Assistant in action:

https://github.com/raselai/skincafe-RAG-app/blob/main/Skrin%20Cafe%20Final.mp4

### Key Features Demonstrated:
- 🤖 AI-powered product recommendations
- 🖼️ Product image display with automatic loading
- 💰 Price information (regular and sale prices)
- 💬 Interactive chat interface with conversation history
- 📱 Mobile-responsive design
- 🔍 Intelligent product search and filtering

## Features

- Text-based product search and recommendations
- Product information retrieval including descriptions, prices, and images
- Interactive Streamlit interface with chat functionality
- Automatic product image display
- Conversation history maintenance
- Mobile-responsive design

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/raselai/skincafe-RAG-app.git
cd skincafe-RAG-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run rag.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. You can:
   - Type questions about products in the chat input
   - Get personalized product recommendations
   - View product images and prices
   - Ask follow-up questions for more details

## Project Structure

- `rag.py`: Main Streamlit application with RAG implementation
- `data/skincafe_products.json`: Product database with SkinCafe products
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not tracked in git)
- `TASK.md`: Project task breakdown
- `PLANNING.md`: Project planning and architecture

## How It Works

1. The application uses FAISS vector database to store product embeddings
2. Text queries are processed using OpenAI's embeddings
3. The RAG system combines retrieved information with GPT-4 to generate responses
4. Responses include product images, prices, and detailed information
5. Chat history is maintained for contextual conversations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 