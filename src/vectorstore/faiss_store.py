
"""
FAISS vector store utilities for Ask Document AI.

This module provides functions to create, save, and load
FAISS vector stores used for document retrieval.
"""

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


# ============================================================
# Create Vector Store
# ============================================================

def create_vectorstore(
    documents: list[Document],
    embeddings: HuggingFaceEmbeddings,
) -> FAISS:
    """
    Create a FAISS vector store from document chunks.

    Args:
        documents:
            Chunked LangChain Document objects.

        embeddings:
            Initialized embedding model.

    Returns:
        FAISS:
            Configured FAISS vector store.

    Raises:
        ValueError:
            If documents or embeddings are missing.

        RuntimeError:
            If FAISS vector store creation fails.
    """

    if not documents:
        raise ValueError(
            "No documents were provided to create the vector store."
        )

    if embeddings is None:
        raise ValueError(
            "An embedding model is required to create the vector store."
        )

    try:
        vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=embeddings,
        )

        return vectorstore

    except Exception as exc:
        raise RuntimeError(
            f"Failed to create FAISS vector store: {exc}"
        ) from exc


# ============================================================
# Save Vector Store
# ============================================================

def save_vectorstore(
    vectorstore: FAISS,
    directory: str | Path,
) -> None:
    """
    Save a FAISS vector store to a local directory.

    Args:
        vectorstore:
            FAISS vector store to save.

        directory:
            Target directory for the FAISS index.

    Raises:
        ValueError:
            If vectorstore is None.

        RuntimeError:
            If the vector store cannot be saved.
    """

    if vectorstore is None:
        raise ValueError(
            "A valid FAISS vector store is required for saving."
        )

    path = Path(directory)

    try:
        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        vectorstore.save_local(str(path))

    except Exception as exc:
        raise RuntimeError(
            f"Failed to save FAISS vector store to "
            f"'{path}': {exc}"
        ) from exc


# ============================================================
# Load Vector Store
# ============================================================

def load_vectorstore(
    directory: str | Path,
    embeddings: HuggingFaceEmbeddings,
) -> FAISS:
    """
    Load a previously saved FAISS vector store.

    The stored index must come from a trusted source because
    FAISS loading may use Python deserialization internally.

    Args:
        directory:
            Directory containing the saved FAISS index.

        embeddings:
            Embedding model compatible with the saved index.

    Returns:
        FAISS:
            Loaded FAISS vector store.

    Raises:
        FileNotFoundError:
            If the vector store directory or index is missing.

        ValueError:
            If the embedding model is missing.

        RuntimeError:
            If loading the vector store fails.
    """

    path = Path(directory)

    if not path.exists():
        raise FileNotFoundError(
            f"Vector store directory not found: {path}"
        )

    if not path.is_dir():
        raise ValueError(
            f"Vector store path is not a directory: {path}"
        )

    if embeddings is None:
        raise ValueError(
            "An embedding model is required to load the vector store."
        )

    # FAISS normally creates these files.
    index_file = path / "index.faiss"
    metadata_file = path / "index.pkl"

    if not index_file.exists():
        raise FileNotFoundError(
            f"FAISS index file not found: {index_file}"
        )

    if not metadata_file.exists():
        raise FileNotFoundError(
            f"FAISS metadata file not found: {metadata_file}"
        )

    try:
        vectorstore = FAISS.load_local(
            str(path),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        return vectorstore

    except Exception as exc:
        raise RuntimeError(
            f"Failed to load FAISS vector store from "
            f"'{path}': {exc}"
        ) from exc
