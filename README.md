# Namma Vivasayam – AI-Powered Farmer Welfare Assistant

## Project Overview

Namma Vivasayam is a bilingual AI-powered farmer welfare assistant developed using Python, LangChain, HuggingFace, FAISS, OpenAI, and Streamlit.

The application is designed to help farmers in Tamil Nadu access information about government agricultural schemes, subsidies, crop insurance, irrigation support, and other welfare benefits.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded PDF documents and generate context-based responses to user queries.

## Key Features

- **Bilingual Support:** Supports English and Tamil for both the user interface and AI-generated responses.
- **Multiple PDF Uploads:** Allows users to upload agricultural scheme documents.
- **AI-Powered Chatbot:** Answers questions based on information retrieved from uploaded PDFs.
- **Voice-Based Questions:** Supports voice input using OpenAI Whisper.
- **Quick Scheme Finder:** Provides information about crop insurance, seed subsidies, farm machinery, and irrigation support.
- **Frequently Asked Questions:** Includes predefined questions for easier access to information.
- **Chat History:** Maintains previous questions and responses during the session.
- **Document References:** Displays relevant PDF filenames and page numbers.
- **Interactive Interface:** Provides a user-friendly Streamlit application.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| LangChain | Document processing and RAG implementation |
| HuggingFace Embeddings | Generating text embeddings |
| FAISS | Vector storage and similarity search |
| OpenAI GPT-4o-mini | Generating context-based responses |
| OpenAI Whisper | Speech-to-text conversion |
| PyPDFLoader | Extracting text from PDF documents |

## Project Structure

```text
Namma_Vivasayam_RAG/
│
├── assets/
│   └── farmer_banner.png
├── pdfs/
├── farmer_faiss_index/
├── config.py
├── rag_engine.py
├── farmer_application.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `pdfs` and `farmer_faiss_index` folders are used locally and excluded from GitHub. The `.env` file containing the OpenAI API key is also excluded for security.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Namma_Vivasayam_RAG.git
cd Namma_Vivasayam_RAG
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

Create a `.env` file in the project directory and add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Application

```bash
python -m streamlit run farmer_application.py
```

Open the local URL displayed in the terminal.

## How the Application Works

1. Users upload PDF documents containing agricultural welfare scheme information.
2. LangChain extracts and splits the PDF content into smaller text chunks.
3. HuggingFace generates vector embeddings for the extracted text.
4. FAISS stores the embeddings and performs similarity searches.
5. Users submit questions through text or voice input.
6. The application retrieves relevant information from the FAISS database.
7. OpenAI generates responses using the retrieved document context.
8. The application displays the response along with available document references.

## Key Learnings

This project provided hands-on experience in:

- Understanding Retrieval-Augmented Generation (RAG).
- Processing multiple PDF documents using LangChain.
- Generating embeddings using HuggingFace models.
- Storing and retrieving document embeddings using FAISS.
- Integrating OpenAI models into a Python application.
- Developing interactive web interfaces using Streamlit.
- Implementing English and Tamil language support.
- Adding voice-based question functionality.
- Debugging API authentication and application interface issues.


## Conclusion

Namma Vivasayam demonstrates how Retrieval-Augmented Generation can be used to develop an AI-powered assistant for accessing agricultural welfare information.

As part of my Generative AI learning journey, this project helped me gain practical knowledge of integrating LangChain, HuggingFace, FAISS, OpenAI, and Streamlit into a functional application.

**Namma Vivasayam – Farmers Prosper, Tamil Nadu Grows.**
