
"""
Tests for the embedding model utilities.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.embeddings.embedder import create_embeddings


# ============================================================
# Tests
# ============================================================

@patch("src.embeddings.embedder.HuggingFaceEmbeddings")
def test_create_embeddings_returns_embedding_model(
    mock_embeddings: MagicMock,
) -> None:
    """
    Verify that the embedding model is initialized successfully.
    """

    mock_instance = MagicMock()
    mock_embeddings.return_value = mock_instance

    embeddings = create_embeddings()

    assert embeddings is mock_instance

    mock_embeddings.assert_called_once()


@patch("src.embeddings.embedder.HuggingFaceEmbeddings")
def test_create_embeddings_uses_configured_model(
    mock_embeddings: MagicMock,
) -> None:
    """
    Verify that the configured embedding model is used.
    """

    from config.settings import EMBEDDING_MODEL

    create_embeddings()

    mock_embeddings.assert_called_once()

    call_kwargs = mock_embeddings.call_args.kwargs

    assert call_kwargs["model_name"] == EMBEDDING_MODEL


@patch("src.embeddings.embedder.HuggingFaceEmbeddings")
def test_create_embeddings_uses_cpu(
    mock_embeddings: MagicMock,
) -> None:
    """
    Verify that the embedding model is configured to use CPU.
    """

    create_embeddings()

    call_kwargs = mock_embeddings.call_args.kwargs

    assert call_kwargs["model_kwargs"]["device"] == "cpu"


@patch("src.embeddings.embedder.HuggingFaceEmbeddings")
def test_create_embeddings_normalizes_embeddings(
    mock_embeddings: MagicMock,
) -> None:
    """
    Verify that embedding normalization is enabled.
    """

    create_embeddings()

    call_kwargs = mock_embeddings.call_args.kwargs

    assert (
        call_kwargs["encode_kwargs"]["normalize_embeddings"]
        is True
    )


@patch("src.embeddings.embedder.HuggingFaceEmbeddings")
def test_create_embeddings_handles_initialization_error(
    mock_embeddings: MagicMock,
) -> None:
    """
    Verify that embedding initialization errors are
    converted into RuntimeError.
    """

    mock_embeddings.side_effect = Exception(
        "Model initialization failed"
    )

    with pytest.raises(RuntimeError, match="Failed to initialize"):
        create_embeddings()
