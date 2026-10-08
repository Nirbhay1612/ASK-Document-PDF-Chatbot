# 📄 Ask Document AI

An AI-powered **PDF question-answering chatbot** that allows users to upload a document and ask questions about its content using natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the uploaded document and generate context-aware responses using a Groq-powered LLM.

---
## 🎞 Demo Link

- **[ASK Document PDF-Chatbot](APP_link)**


## 🚀 Features

- 📄 Upload PDF documents
- ✂️ Automatically split documents into smaller chunks
- 🧠 Generate semantic embeddings using Hugging Face Sentence Transformers
- 🔎 Perform similarity search using FAISS
- 🤖 Generate document-grounded answers using Groq LLM
- 💬 Interactive Streamlit chat interface
- 🗂️ Maintain conversation history during the current session
- ⚙️ Configure the number of retrieved document chunks
- 📑 Display relevant source pages when available
- 🔐 Secure API key management using environment variables
- 🧪 Automated tests using Pytest
- 🧩 Modular and maintainable project architecture

---


## 📁 Project Structure

```text
AskDocument-PDF-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── uploads/
│   │   └── .gitkeep
│   └── vectorstore/
│       └── .gitkeep
│
├── src/
│   ├── __init__.py
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── prompts.py
│   │   └── response_handler.py
│   │
│   ├── document/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── splitter.py
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedder.py
│   │
│   ├── vectorstore/
│   │   ├── __init__.py
│   │   └── faiss_store.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── validators.py
│
└── tests/
    ├── __init__.py
    ├── test_loader.py
    ├── test_splitter.py
    ├── test_embeddings.py
    └── test_rag.py
```

---

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Sentence%20Transformers-yellow?logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-00ADD8)
![PyPDF](https://img.shields.io/badge/PyPDF-PDF%20Processing-red)
![python-dotenv](https://img.shields.io/badge/python--dotenv-Environment%20Variables-green)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)

## 🔄 How It Works

### 1. 📄 Upload PDF

The user uploads a PDF through the Streamlit interface.

### 2. 📖 Load Document

The PDF loader extracts text and metadata from the document.

### 3. ✂️ Split Text

The extracted content is divided into smaller chunks using a recursive text splitter.

### 4. 🧠 Generate Embeddings

Each text chunk is converted into a numerical vector representation using a Hugging Face Sentence Transformer model.

### 5. 🔎 Store Embeddings

The generated embeddings are stored in a FAISS vector store for efficient similarity search.

### 6. 🔍 Retrieve Relevant Context

When the user asks a question, FAISS searches for the most relevant document chunks.

### 7. 🤖 Generate Answer

The retrieved context and user question are passed to the Groq-powered LLM.

The model generates an answer based on the retrieved document content.

### 8. 📑 Display Sources

When page metadata is available, the application displays the relevant document pages along with the response.

---






## 🚧 Future Improvements

- [ ] Support multiple PDF uploads
- [ ] Persistent vector database
- [ ] Persistent conversation memory
- [ ] Improved source/page citations
- [ ] Streaming responses
- [ ] Document preview
- [ ] Authentication
- [ ] Cloud deployment
- [ ] Support for additional document formats
- [ ] Improved retrieval and reranking
- [ ] OCR support for scanned PDFs

---

## 🎯 Project Goal

The goal of this project is to demonstrate the implementation of a modular, production-oriented **Retrieval-Augmented Generation (RAG) application** using modern AI, LLM, embedding, and vector-search technologies.

The project focuses on:

- Clean modular architecture
- Document ingestion
- Semantic search
- Retrieval-Augmented Generation
- Error handling
- Configuration management
- Automated testing
- Secure environment configuration

---

## 👨‍💻 Author

**Nirbhay Tembhurne**

Python Developer | AI Chatbot | AI Integration | Automation

---


