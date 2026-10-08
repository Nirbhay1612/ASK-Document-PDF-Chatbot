
"""
Document text splitting utilities for Ask Document AI.

This module converts loaded documents into smaller, searchable
chunks suitable for embedding and vector retrieval.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE


def split_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Split documents into smaller chunks for vector retrieval.

    Args:
        documents:
            List of LangChain Document objects.

    Returns:
        List of chunked LangChain Document objects.

    Raises:
        ValueError:
            If no documents are provided or no chunks are generated.
    """

    # ------------------------------------------------------
    # Validate input
    # ------------------------------------------------------

    if not documents:
        raise ValueError(
            "No documents were provided for splitting."
        )

    # ------------------------------------------------------
    # Create text splitter
    # ------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    # ------------------------------------------------------
    # Split documents
    # ------------------------------------------------------

    chunks = splitter.split_documents(documents)

    # ------------------------------------------------------
    # Validate output
    # ------------------------------------------------------

    if not chunks:
        raise ValueError(
            "Document splitting produced no chunks."
        )

    # Remove chunks containing only whitespace
    chunks = [
        chunk
        for chunk in chunks
        if chunk.page_content.strip()
    ]

    if not chunks:
        raise ValueError(
            "No readable text chunks were generated."
        )

    return chunks
