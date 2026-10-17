# 📄 Ask Document AI — PDF Question Answering Chatbot

An AI-powered **PDF Question Answering Chatbot** that allows users to upload PDF documents and ask questions about their content using natural language.

Built with **Python, Streamlit, LangChain, Hugging Face Sentence Transformers, FAISS, and Groq**, this application uses Retrieval-Augmented Generation (RAG) to retrieve relevant document context and generate context-aware answers.

---

## 🎞️ Live Demo

🚀 **[Try Ask Document AI](https://ask-document-pdf-chatbot-otdrljsldvgfe3jxm8qhu5.streamlit.app/)**

Upload a PDF, ask questions about its content, and explore AI-powered document question answering.

---

## 📸 Application Screenshots

### 1. Application Interface

The main interface for uploading documents and interacting with the chatbot.

![Ask Document AI - Application Interface](screenshots/app-home.png)

### 2. PDF Document Upload

Upload a PDF document to begin the document processing pipeline.

![PDF Document Upload](screenshots/pdf-upload.png)

### 3. Chat and AI Response

Ask questions about your document and receive context-aware answers.

![Chat Response](screenshots/chat-response.png)

### 4. Source References

Review source-page references when available in the retrieved document context.

![Source References](screenshots/source-citations.png)

---

## ✨ Features

- 📄 Upload PDF documents
- 📖 Extract text and document metadata
- ✂️ Split documents into manageable text chunks
- 🧠 Generate semantic embeddings using Hugging Face Sentence Transformers
- 🔎 Perform similarity search using FAISS
- 🤖 Generate document-grounded answers using a Groq-powered LLM
- 💬 Interactive Streamlit chat interface
- 🗂️ Maintain conversation history during the current session
- ⚙️ Configure the number of retrieved document chunks
- 📑 Display relevant source pages when available
- 🔐 Manage API keys through environment variables
- 🧪 Automated testing with Pytest
- 🧩 Modular and maintainable project architecture

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| LangChain | Document processing and RAG components |
| Hugging Face Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Groq | LLM-powered answer generation |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |
| Pytest | Automated testing |

---

## 🏗️ Project Structure

```text
AskDocument-PDF-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── uploads/
│   └── vectorstore/
│
├── screenshots/
│   ├── app-home.png
│   ├── pdf-upload.png
│   ├── chat-response.png
│   └── source-citations.png
│
├── src/
│   ├── __init__.py
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