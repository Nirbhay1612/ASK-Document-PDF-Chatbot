
"""
Embedding utilities for Ask Document AI.

This module initializes the Hugging Face embedding model
used to convert document chunks into vector representations.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings

from config.settings import EMBEDDING_MODEL


def create_embeddings() -> HuggingFaceEmbeddings:
    """
    Create and return the configured Hugging Face embedding model.

    Returns:
        HuggingFaceEmbeddings:
            Initialized embedding model.

    Raises:
        RuntimeError:
            If the embedding model cannot be initialized.
    """

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

        return embeddings

    except Exception as exc:
        raise RuntimeError(
            f"Failed to initialize embedding model "
            f"'{EMBEDDING_MODEL}': {exc}"
        ) from exc
