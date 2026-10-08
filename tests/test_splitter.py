
"""
Tests for document text splitting.
"""

import pytest
from langchain_core.documents import Document

from src.document.splitter import split_documents


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def sample_documents() -> list[Document]:
    """
    Create sample documents for testing.
    """

    return [
        Document(
            page_content=(
                "Ask Document AI is a PDF question-answering "
                "application. "
                "It uses document retrieval to find relevant "
                "information. "
                "The retrieved information is then provided "
                "to the language model."
            ),
            metadata={
                "page": 0,
                "source": "sample.pdf",
            },
        )
    ]


# ============================================================
# Tests
# ============================================================

def test_split_documents_returns_chunks(
    sample_documents: list[Document],
) -> None:
    """
    Verify that documents are successfully split into chunks.
    """

    chunks = split_documents(sample_documents)

    assert chunks
    assert isinstance(chunks, list)

    assert all(
        isinstance(chunk, Document)
        for chunk in chunks
    )


def test_split_documents_preserves_content(
    sample_documents: list[Document],
) -> None:
    """
    Verify that generated chunks contain text.
    """

    chunks = split_documents(sample_documents)

    assert all(
        chunk.page_content.strip()
        for chunk in chunks
    )


def test_split_documents_preserves_metadata(
    sample_documents: list[Document],
) -> None:
    """
    Verify that document metadata is preserved.
    """

    chunks = split_documents(sample_documents)

    assert chunks

    for chunk in chunks:
        assert "source" in chunk.metadata
        assert "page" in chunk.metadata


def test_split_documents_rejects_empty_input() -> None:
    """
    Verify that empty document input raises ValueError.
    """

    with pytest.raises(ValueError):
        split_documents([])


def test_split_documents_handles_multiple_documents() -> None:
    """
    Verify that multiple documents can be split.
    """

    documents = [
        Document(
            page_content=(
                "This is the first document. "
                "It contains some useful information."
            ),
            metadata={"page": 0},
        ),
        Document(
            page_content=(
                "This is the second document. "
                "It contains additional information."
            ),
            metadata={"page": 1},
        ),
    ]

    chunks = split_documents(documents)

    assert chunks
    assert len(chunks) >= 2


def test_split_documents_removes_empty_chunks() -> None:
    """
    Verify that whitespace-only documents do not produce
    usable chunks.
    """

    documents = [
        Document(
            page_content="   \n\n   ",
            metadata={"page": 0},
        )
    ]

    with pytest.raises(ValueError):
        split_documents(documents)
