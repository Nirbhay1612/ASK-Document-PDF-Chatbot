
"""
PDF document loading utilities for Ask Document AI.

This module handles PDF validation and converts PDF pages
into LangChain Document objects.
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(file_path: str | Path) -> list[Document]:
    """
    Load a PDF file and return its pages as LangChain Documents.

    Args:
        file_path: Path to the PDF file.

    Returns:
        List of LangChain Document objects.

    Raises:
        FileNotFoundError:
            If the PDF file does not exist.

        ValueError:
            If the file is not a PDF or contains no readable content.

        RuntimeError:
            If the PDF loader fails.
    """

    # ------------------------------------------------------
    # Convert input to Path
    # ------------------------------------------------------

    path = Path(file_path)

    # ------------------------------------------------------
    # Validate file existence
    # ------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Expected a PDF file, but received: {path}"
        )

    # ------------------------------------------------------
    # Validate file extension
    # ------------------------------------------------------

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    # ------------------------------------------------------
    # Load PDF
    # ------------------------------------------------------

    try:
        loader = PyPDFLoader(str(path))
        documents = loader.load()

    except Exception as exc:
        raise RuntimeError(
            f"Failed to load PDF '{path.name}': {exc}"
        ) from exc

    # ------------------------------------------------------
    # Validate loaded documents
    # ------------------------------------------------------

    if not documents:
        raise ValueError(
            "The PDF does not contain any readable pages."
        )

    # ------------------------------------------------------
    # Remove completely empty pages
    # ------------------------------------------------------

    readable_documents = [
        document
        for document in documents
        if document.page_content.strip()
    ]

    if not readable_documents:
        raise ValueError(
            "The PDF contains no readable text."
        )

    return readable_documents
