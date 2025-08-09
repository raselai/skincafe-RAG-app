# Cosmetics E-commerce RAG Assistant

A multimodal Retrieval-Augmented Generation (RAG) application for a cosmetics e-commerce platform. This application allows customers to ask questions about products and find similar items using both text and image queries.

## Features

- Text-based product search and recommendations
- Image-based product search using CLIP embeddings
- Product information retrieval including descriptions, prices, and images
- Interactive Streamlit interface
- Support for both text and image queries

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
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
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. You can:
   - Type questions about products in the text input
   - Upload images to find similar products
   - Get product recommendations with images and prices

## Project Structure

- `app.py`: Main Streamlit application
- `rag_engine.py`: RAG implementation with text and image search capabilities
- `data/skincafe_products.json`: Product database
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not tracked in git)

## How It Works

1. The application uses ChromaDB to store product embeddings
2. Text queries are processed using OpenAI's embeddings
3. Image queries are processed using CLIP embeddings
4. The RAG system combines retrieved information with GPT-3.5-turbo to generate responses
5. Responses include product images and links when relevant

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 