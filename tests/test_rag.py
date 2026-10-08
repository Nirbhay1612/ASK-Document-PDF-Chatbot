
"""
Tests for the RAG chatbot.
"""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from src.chatbot.chatbot import (
    DocumentChatbot,
    create_chatbot,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def sample_documents() -> list[Document]:
    """
    Create sample retrieved documents.
    """

    return [
        Document(
            page_content=(
                "Ask Document AI is a PDF question-answering "
                "application."
            ),
            metadata={
                "page": 0,
                "source": "sample.pdf",
            },
        ),
        Document(
            page_content=(
                "The application uses document retrieval "
                "to answer questions."
            ),
            metadata={
                "page": 1,
                "source": "sample.pdf",
            },
        ),
    ]


@pytest.fixture
def mock_vectorstore() -> MagicMock:
    """
    Create a mocked vector store and retriever.
    """

    vectorstore = MagicMock()
    retriever = MagicMock()

    vectorstore.as_retriever.return_value = retriever

    return vectorstore


# ============================================================
# Constructor Tests
# ============================================================

@patch("src.chatbot.chatbot.ChatGroq")
def test_create_chatbot_success(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
) -> None:
    """
    Verify that the chatbot can be created successfully.
    """

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
        top_k=4,
    )

    assert isinstance(
        chatbot,
        DocumentChatbot,
    )

    assert chatbot.vectorstore is mock_vectorstore
    assert chatbot.top_k == 4

    mock_chat_groq.assert_called_once()


def test_create_chatbot_rejects_none_vectorstore() -> None:
    """
    Verify that a missing vector store raises ValueError.
    """

    with pytest.raises(
        ValueError,
        match="Vector store cannot be None",
    ):
        create_chatbot(
            vectorstore=None,
        )


@patch("src.chatbot.chatbot.ChatGroq")
def test_create_chatbot_rejects_invalid_top_k(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
) -> None:
    """
    Verify that invalid top_k values are rejected.
    """

    with pytest.raises(
        ValueError,
        match="top_k must be greater",
    ):
        create_chatbot(
            vectorstore=mock_vectorstore,
            top_k=0,
        )


# ============================================================
# Context Tests
# ============================================================

def test_build_context(
    sample_documents: list[Document],
) -> None:
    """
    Verify that retrieved documents are converted
    into a formatted context string.
    """

    context = DocumentChatbot.build_context(
        sample_documents
    )

    assert "Document Chunk 1" in context
    assert "Document Chunk 2" in context

    assert (
        "Ask Document AI is a PDF question-answering"
        in context
    )

    assert (
        "document retrieval"
        in context
    )


def test_build_context_empty_documents() -> None:
    """
    Verify that empty document input returns an empty string.
    """

    context = DocumentChatbot.build_context([])

    assert context == ""


# ============================================================
# Retrieval Tests
# ============================================================

@patch("src.chatbot.chatbot.ChatGroq")
def test_retrieve_documents(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
    sample_documents: list[Document],
) -> None:
    """
    Verify that relevant documents are retrieved.
    """

    retriever = mock_vectorstore.as_retriever.return_value

    retriever.invoke.return_value = sample_documents

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
        top_k=4,
    )

    documents = chatbot.retrieve_documents(
        "What is Ask Document AI?"
    )

    assert documents == sample_documents

    retriever.invoke.assert_called_once_with(
        "What is Ask Document AI?"
    )


@patch("src.chatbot.chatbot.ChatGroq")
def test_retrieve_documents_empty_question(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
) -> None:
    """
    Verify that an empty question does not trigger retrieval.
    """

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
    )

    documents = chatbot.retrieve_documents("   ")

    assert documents == []


# ============================================================
# Ask / RAG Tests
# ============================================================

@patch("src.chatbot.chatbot.ChatGroq")
def test_ask_generates_response(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
    sample_documents: list[Document],
) -> None:
    """
    Verify the complete RAG answer generation flow.
    """

    retriever = mock_vectorstore.as_retriever.return_value

    retriever.invoke.return_value = sample_documents

    mock_llm = mock_chat_groq.return_value

    mock_response = MagicMock()
    mock_response.content = (
        "Ask Document AI is a PDF question-answering application."
    )

    mock_llm.invoke.return_value = mock_response

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
        top_k=4,
    )

    answer = chatbot.ask(
        "What is Ask Document AI?"
    )

    assert (
        "PDF question-answering application"
        in answer
    )

    mock_llm.invoke.assert_called_once()


@patch("src.chatbot.chatbot.ChatGroq")
def test_ask_empty_question(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
) -> None:
    """
    Verify that an empty question returns a friendly message.
    """

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
    )

    answer = chatbot.ask("   ")

    assert answer == "Please enter a question."


@patch("src.chatbot.chatbot.ChatGroq")
def test_ask_when_no_documents_found(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
) -> None:
    """
    Verify the fallback response when retrieval finds nothing.
    """

    retriever = mock_vectorstore.as_retriever.return_value

    retriever.invoke.return_value = []

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
    )

    answer = chatbot.ask(
        "What information is available?"
    )

    assert (
        "couldn't find relevant information"
        in answer
    )


@patch("src.chatbot.chatbot.ChatGroq")
def test_ask_handles_llm_error(
    mock_chat_groq: MagicMock,
    mock_vectorstore: MagicMock,
    sample_documents: list[Document],
) -> None:
    """
    Verify that LLM errors are converted into RuntimeError.
    """

    retriever = mock_vectorstore.as_retriever.return_value

    retriever.invoke.return_value = sample_documents

    mock_llm = mock_chat_groq.return_value

    mock_llm.invoke.side_effect = Exception(
        "LLM request failed"
    )

    chatbot = create_chatbot(
        vectorstore=mock_vectorstore,
    )

    with pytest.raises(
        RuntimeError,
        match="Failed to generate chatbot response",
    ):
        chatbot.ask(
            "What is this document about?"
        )
