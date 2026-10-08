
import hashlib
import os
import sys
import tempfile

import streamlit as st
from dotenv import load_dotenv


# ============================================================
# Project Configuration
# ============================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ============================================================
# Environment Variables
# ============================================================

load_dotenv()


# ============================================================
# Internal Imports
# ============================================================

from src.chatbot.chatbot import create_chatbot
from src.document.loader import load_pdf
from src.document.splitter import split_documents
from src.embeddings.embedder import create_embeddings
from src.vectorstore.faiss_store import create_vectorstore


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Ask Document AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Session State
# ============================================================

DEFAULT_SESSION_STATE = {
    "vectorstore": None,
    "chatbot": None,
    "messages": [],
    "document_hash": None,
    "document_name": None,
}

for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# Helper Functions
# ============================================================

def get_file_hash(uploaded_file) -> str:
    """Generate a unique hash for the uploaded document."""
    file_bytes = uploaded_file.getvalue()
    return hashlib.md5(file_bytes).hexdigest()


def reset_document_state() -> None:
    """Clear the current document and chat state."""
    st.session_state.vectorstore = None
    st.session_state.chatbot = None
    st.session_state.messages = []
    st.session_state.document_hash = None
    st.session_state.document_name = None


def process_document(uploaded_file, top_k: int) -> None:
    """Process the uploaded PDF and initialize the chatbot."""

    file_hash = get_file_hash(uploaded_file)

    # Avoid re-processing the same PDF
    if (
        st.session_state.document_hash == file_hash
        and st.session_state.chatbot is not None
    ):
        return

    temp_pdf_path = None

    try:
        with st.spinner("📄 Processing your document..."):

            # ------------------------------------------------
            # Save uploaded PDF temporarily
            # ------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                temp_pdf_path = temp_file.name

            # ------------------------------------------------
            # 1. Load PDF
            # ------------------------------------------------

            documents = load_pdf(temp_pdf_path)

            if not documents:
                raise ValueError(
                    "No readable content was found in the PDF."
                )

            # ------------------------------------------------
            # 2. Split document
            # ------------------------------------------------

            chunks = split_documents(documents)

            if not chunks:
                raise ValueError(
                    "The document could not be split into text chunks."
                )

            # ------------------------------------------------
            # 3. Create embeddings
            # ------------------------------------------------

            embeddings = create_embeddings()

            # ------------------------------------------------
            # 4. Create vector store
            # ------------------------------------------------

            vectorstore = create_vectorstore(
                chunks,
                embeddings,
            )

            # ------------------------------------------------
            # 5. Create chatbot
            # ------------------------------------------------

            chatbot = create_chatbot(
                vectorstore=vectorstore,
                top_k=top_k,
            )

            # ------------------------------------------------
            # Store application state
            # ------------------------------------------------

            st.session_state.vectorstore = vectorstore
            st.session_state.chatbot = chatbot
            st.session_state.document_hash = file_hash
            st.session_state.document_name = uploaded_file.name
            st.session_state.messages = []

        st.success(
            f"✅ **{uploaded_file.name}** processed successfully!"
        )

    except Exception as error:
        st.error(
            "❌ Unable to process the document. "
            "Please make sure the PDF is valid and try again."
        )

        with st.expander("Show technical details"):
            st.code(str(error))

        reset_document_state()

    finally:
        # Always remove temporary file
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)


# ============================================================
# Header
# ============================================================

st.title("📄 Ask Document AI")

st.markdown(
    """
    Upload a PDF and ask questions about its content.

    **Ask Document AI** uses document retrieval and an AI model
    to generate answers based on the uploaded document.
    """
)

st.divider()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("📁 Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        help="Upload a PDF document to start chatting.",
    )

    st.divider()

    st.subheader("⚙️ Settings")

    top_k = st.slider(
        "Retrieved chunks",
        min_value=1,
        max_value=10,
        value=4,
        help="Number of relevant document chunks retrieved for each question.",
    )

    st.divider()

    if st.session_state.document_name:

        st.caption(
            f"📄 Current document: "
            f"**{st.session_state.document_name}**"
        )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# Document Processing
# ============================================================

if uploaded_file is not None:

    process_document(
        uploaded_file=uploaded_file,
        top_k=top_k,
    )


# ============================================================
# Chat Interface
# ============================================================

if st.session_state.chatbot is not None:

    st.subheader("💬 Chat with your document")

    # --------------------------------------------------------
    # Display conversation history
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------------------------------------------------------
    # User question
    # --------------------------------------------------------

    user_question = st.chat_input(
        "Ask something about your document..."
    )

    if user_question:

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        # ----------------------------------------------------
        # Generate AI response
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner("🤔 Thinking..."):

                try:

                    response = st.session_state.chatbot.ask(
                        user_question
                    )

                    st.markdown(response)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )

                except Exception as error:

                    st.error(
                        "❌ I couldn't generate an answer. "
                        "Please try asking your question again."
                    )

                    with st.expander("Show technical details"):
                        st.code(str(error))


# ============================================================
# Empty State
# ============================================================

else:

    st.info(
        "👈 Upload a PDF from the sidebar to start chatting."
    )

    st.markdown(
        """
        ### 🚀 How it works

        1. 📤 Upload a PDF
        2. 🔎 Extract and split the document
        3. 🧠 Generate embeddings
        4. 🗄️ Store vectors in FAISS
        5. 💬 Ask questions
        6. 🤖 Get answers based on your document
        """
    )
