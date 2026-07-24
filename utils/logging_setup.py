"""
Logging configuration for CandidateOps.
Sets up structured logging with console and rotating file handlers.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from infrastructure.config.settings import settings


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure logging for the application.

    Args:
        name: Logger name. If None, returns the root logger.

    Returns:
        Configured logger instance.
    """
    # Get logger
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Set logging level
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        fmt=settings.logging.format,
        datefmt=settings.logging.date_format
    )

    # Console handler
    if settings.logging.console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler with rotation
    if settings.logging.file_enabled:
        # Ensure log directory exists
        log_file_path = Path(settings.logging.file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=settings.logging.max_bytes,
            backupCount=settings.logging.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    Args:
        name: Logger name (usually __module__)

    Returns:
        Configured logger instance.
    """
    return setup_logging(name)