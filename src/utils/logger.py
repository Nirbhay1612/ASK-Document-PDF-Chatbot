
"""
Application logging utilities for Ask Document AI.

This module provides a centralized logger configuration
for consistent logging across the application.
"""

import logging
from pathlib import Path


# ============================================================
# Logging Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Logger Formatter
# ============================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================
# Logger Factory
# ============================================================

def get_logger(
    name: str = "ask_document_ai",
) -> logging.Logger:
    """
    Create or return a configured application logger.

    Args:
        name:
            Name of the logger.

    Returns:
        Configured logging.Logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers when Streamlit reloads
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # --------------------------------------------------------
    # Console Handler
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(
        logging.INFO
    )

    console_handler.setFormatter(
        formatter
    )

    # --------------------------------------------------------
    # File Handler
    # --------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(
        logging.INFO
    )

    file_handler.setFormatter(
        formatter
    )

    # --------------------------------------------------------
    # Register handlers
    # --------------------------------------------------------

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )

    return logger
