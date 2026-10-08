
"""
Validation utilities for Ask Document AI.

This module contains reusable validation functions for
uploaded files, user questions, and application settings.
"""

from pathlib import Path
from typing import Any


# ============================================================
# Constants
# ============================================================

DEFAULT_MAX_FILE_SIZE_MB = 10
MIN_TOP_K = 1
MAX_TOP_K = 10


# ============================================================
# PDF Validation
# ============================================================

def validate_pdf_file(
    file_path: str | Path,
    max_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB,
) -> None:
    """
    Validate a PDF file before processing.

    Args:
        file_path:
            Path to the PDF file.

        max_size_mb:
            Maximum allowed file size in megabytes.

    Raises:
        FileNotFoundError:
            If the file does not exist.

        ValueError:
            If the file is invalid or exceeds the size limit.
    """

    path = Path(file_path)

    # --------------------------------------------------------
    # Check existence
    # --------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if not path.is_file():
        raise ValueError(
            f"Expected a file, but received: {path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    # --------------------------------------------------------
    # Check file size
    # --------------------------------------------------------

    file_size_mb = (
        path.stat().st_size / (1024 * 1024)
    )

    if file_size_mb > max_size_mb:
        raise ValueError(
            f"PDF size ({file_size_mb:.2f} MB) exceeds "
            f"the maximum allowed size of {max_size_mb} MB."
        )


# ============================================================
# Uploaded File Validation
# ============================================================

def validate_uploaded_file(
    uploaded_file: Any,
    max_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB,
) -> None:
    """
    Validate a Streamlit uploaded file.

    Args:
        uploaded_file:
            Streamlit UploadedFile object.

        max_size_mb:
            Maximum allowed file size in megabytes.

    Raises:
        ValueError:
            If the uploaded file is invalid.
    """

    if uploaded_file is None:
        raise ValueError(
            "No file was uploaded."
        )

    file_name = getattr(
        uploaded_file,
        "name",
        "",
    )

    if not file_name:
        raise ValueError(
            "Uploaded file has no valid filename."
        )

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    if Path(file_name).suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    # --------------------------------------------------------
    # Validate file size
    # --------------------------------------------------------

    file_size = getattr(
        uploaded_file,
        "size",
        None,
    )

    if file_size is not None:

        file_size_mb = (
            file_size / (1024 * 1024)
        )

        if file_size_mb > max_size_mb:
            raise ValueError(
                f"File size ({file_size_mb:.2f} MB) exceeds "
                f"the maximum allowed size of "
                f"{max_size_mb} MB."
            )


# ============================================================
# Question Validation
# ============================================================

def validate_question(
    question: str,
) -> str:
    """
    Validate and normalize a user's question.

    Args:
        question:
            User-entered question.

    Returns:
        Cleaned question.

    Raises:
        ValueError:
            If the question is empty or invalid.
    """

    if not isinstance(question, str):
        raise ValueError(
            "Question must be a text string."
        )

    cleaned_question = question.strip()

    if not cleaned_question:
        raise ValueError(
            "Question cannot be empty."
        )

    return cleaned_question


# ============================================================
# Top-K Validation
# ============================================================

def validate_top_k(
    top_k: int,
) -> int:
    """
    Validate the number of document chunks to retrieve.

    Args:
        top_k:
            Number of chunks to retrieve.

    Returns:
        Validated top_k value.

    Raises:
        ValueError:
            If top_k is outside the allowed range.
    """

    if not isinstance(top_k, int):
        raise ValueError(
            "top_k must be an integer."
        )

    if not MIN_TOP_K <= top_k <= MAX_TOP_K:
        raise ValueError(
            f"top_k must be between "
            f"{MIN_TOP_K} and {MAX_TOP_K}."
        )

    return top_k
