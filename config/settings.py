
"""
Central configuration for Ask Document AI.

All environment variables and application-level settings
are managed from this module.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv(BASE_DIR / ".env")


# ==========================================================
# Helper Functions
# ==========================================================

def get_int_env(
    name: str,
    default: int,
    minimum: int | None = None,
) -> int:
    """
    Read an integer environment variable safely.
    """

    value = os.getenv(name, str(default))

    try:
        result = int(value)
    except ValueError as error:
        raise ValueError(
            f"{name} must be a valid integer. "
            f"Received: {value!r}"
        ) from error

    if minimum is not None and result < minimum:
        raise ValueError(
            f"{name} must be >= {minimum}. "
            f"Received: {result}"
        )

    return result


# ==========================================================
# Groq Configuration
# ==========================================================

GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

GROQ_MODEL: str = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant",
)


# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)


# ==========================================================
# Document Chunking
# ==========================================================

CHUNK_SIZE: int = get_int_env(
    "CHUNK_SIZE",
    default=700,
    minimum=100,
)

CHUNK_OVERLAP: int = get_int_env(
    "CHUNK_OVERLAP",
    default=100,
    minimum=0,
)

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError(
        "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
    )


# ==========================================================
# Retrieval Configuration
# ==========================================================

TOP_K: int = get_int_env(
    "TOP_K",
    default=5,
    minimum=1,
)


# ==========================================================
# Application Configuration
# ==========================================================

MAX_UPLOAD_SIZE_MB: int = get_int_env(
    "MAX_UPLOAD_SIZE_MB",
    default=10,
    minimum=1,
)


# ==========================================================
# Directory Initialization
# ==========================================================

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

VECTORSTORE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
