# 📄 Ask Document AI — PDF Question Answering Chatbot

An AI-powered **PDF Question Answering Chatbot** that enables users to upload PDF documents and ask questions about their content using natural language.

Built using Python, Streamlit, LangChain, Hugging Face Sentence Transformers, FAISS, and Groq, this project implements a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant document context and generate context-aware answers.

The application demonstrates practical skills in AI application development, semantic search, document processing, LLM integration, and modular Python development.

---

## 🎯 Project Overview

Ask Document AI simplifies the process of extracting information from PDF documents.

Instead of manually searching through lengthy documents, users can upload a PDF and ask questions in natural language. The application retrieves relevant document chunks and uses a language model to generate responses based on the retrieved context.

**Project objective:** Build a modular, user-friendly document question-answering application using modern AI and retrieval technologies.

---

## 🎞️ Live Demo

🚀 **[Try Ask Document AI](https://ask-document-pdf-chatbot-otdrljsldvgfe3jxm8qhu5.streamlit.app/)**

Upload a PDF, ask questions about its contents, and explore the document question-answering workflow.

---

## 📸 Application Screenshots

### 1. Application Interface

The main interface for uploading PDF documents and interacting with the chatbot.

![Application Interface](screenshots/app-home.png)

### 2. PDF Document Upload

Upload a PDF document to begin processing its contents.

![PDF Upload](screenshots/pdf-upload.png)

### 3. Chat and AI Response

Ask questions and receive responses generated using retrieved document context.

![Chat Response](screenshots/chat-response.png)

### 4. Source References

Review source-page references when available.

![Source References](screenshots/source-citations.png)

### 5. Additional Application Screenshots

If additional screenshots are available in the repository, add them below.

<!-- Example:
![Error Handling](screenshots/error-handling.png)
![Document Processing](screenshots/pdf-processing.png)
-->

---

## ✨ Key Features

- 📄 PDF document upload
- 📖 Text extraction and document metadata processing
- ✂️ Text chunking for efficient retrieval
- 🧠 Semantic embeddings using Hugging Face Sentence Transformers
- 🔎 Similarity search using FAISS
- 🤖 LLM-powered answer generation using Groq
- 💬 Interactive Streamlit chat interface
- 🗂️ Conversation history during the current session
- ⚙️ Configurable retrieval settings
- 📑 Source-page references when available
- 🔐 Environment-based API key configuration
- 🧪 Automated testing with Pytest
- 🧩 Modular and maintainable project structure

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| LangChain | RAG and document-processing components |
| Hugging Face Sentence Transformers | Semantic text embeddings |
| FAISS | Vector similarity search |
| Groq | Language model integration |
| PyPDF | PDF text extraction |
| python-dotenv | Environment variable management |
| Pytest | Automated testing |

---

## 🏗️ Project Architecture

The application follows a modular architecture that separates document processing, embedding generation, vector retrieval, chatbot logic, and configuration.

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
```

> The structure above is illustrative. Update it to match the files and directories actually present in your repository.

---

## 🔄 How It Works

Ask Document AI follows a Retrieval-Augmented Generation (RAG) workflow.

```text
         PDF Upload
              |
              v
       Document Loading
              |
              v
        Text Extraction
              |
              v
         Text Chunking
              |
              v
      Embedding Generation
              |
              v
       FAISS Vector Store
              |
              v
      Similarity Retrieval
              |
              v
      Relevant Document Context
              |
              v
           Groq LLM
              |
              v
      Generated Answer
              |
              v
       Source References
```

### Pipeline Explanation

**1. Document Loading**

The application loads the uploaded PDF and extracts its readable text and metadata.

**2. Text Chunking**

Extracted text is divided into smaller chunks to support relevant document retrieval.

**3. Embedding Generation**

Hugging Face Sentence Transformers converts text chunks into numerical vector representations.

**4. Vector Storage**

FAISS indexes the embeddings to support similarity-based searches.

**5. Context Retrieval**

When a user asks a question, the application retrieves relevant document chunks.

**6. Answer Generation**

The retrieved context and question are passed to a Groq-powered language model to generate an answer.

**7. Response Display**

The generated answer is displayed in the Streamlit interface, with source-page references when available.

---

## ⚙️ Setup Instructions

Follow these steps to run the application locally.

### Prerequisites

Install the following before getting started:

- Python 3.11 or another Python version compatible with the project dependencies
- Git
- Visual Studio Code (recommended)
- A Groq API key

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd AskDocument-PDF-Chatbot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

### Step 2: Create a Virtual Environment

**Windows — PowerShell**

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Wait for the installation to complete before proceeding.

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory of the project.

Add the following configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual Groq API key.

You can obtain an API key from the [Groq Console](https://console.groq.com/).

**Security requirements:**

- Never commit your real `.env` file to GitHub.
- Keep `.env` listed in `.gitignore`.
- Use `.env.example` to document the required environment variables without exposing credentials.

Example `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

If the application uses additional environment variables, document those variables in `.env.example` as well.

### Step 5: Run the Application

From the project root directory, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, typically:

```text
http://localhost:8501
```

Open this URL in your browser.

### Step 6: Use the Application

1. Open the application.
2. Upload a supported PDF document.
3. Wait for document processing and indexing to finish.
4. Enter a question about the uploaded document.
5. Review the generated answer.
6. Check source-page references when available.
7. Ask follow-up questions during the current session.

---

## 🧪 Running Tests

The project includes a Pytest-based test suite for testing supported application components.

Activate the virtual environment before running the tests.

Run the complete test suite:

```bash
pytest -v
```

Run an individual test module:

```bash
pytest tests/test_loader.py -v
```

### Optional: Test Coverage

Install the coverage plugin:

```bash
pip install pytest-cov
```

Generate a coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

Test commands and module names should match the actual test files in the repository.

---

## 🔐 Security and Best Practices

- Store API keys and secrets in environment variables.
- Never expose API keys in source code or public repositories.
- Keep `.env`, virtual environments, caches, and temporary files out of version control.
- Validate uploaded documents before processing.
- Handle invalid or unreadable PDFs gracefully.
- Avoid logging sensitive document contents or credentials.
- Do not upload confidential documents to an untrusted environment.
- Review dependency compatibility before upgrading packages.

---

## 🚧 Future Enhancements

Potential improvements include:

- [ ] Multiple PDF uploads
- [ ] Persistent vector storage
- [ ] Persistent conversation history
- [ ] Improved source citations
- [ ] Streaming responses
- [ ] Document preview
- [ ] Authentication and access control
- [ ] Improved retrieval and reranking
- [ ] OCR support for scanned PDFs
- [ ] Additional document formats

These items represent possible future work, not necessarily existing functionality.

---

## 🎓 Skills Demonstrated

This project demonstrates practical experience with:

- Python application development
- Building interactive applications with Streamlit
- Integrating large language models through APIs
- Retrieval-Augmented Generation (RAG)
- Document loading and text chunking
- Semantic embeddings and vector similarity search
- Modular code organization
- Environment variable management
- Error handling and automated testing
- Git and GitHub project documentation

---

## 👨‍💻 Author

**Nirbhay Tembhurne**

Python Developer | AI Chatbots | AI Integration | AI Automation

---

## ⭐ Support

If you find this project useful, consider giving the repository a star.

Feedback and suggestions for improvement are welcome.