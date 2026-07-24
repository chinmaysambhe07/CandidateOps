"""
Utility helper functions for CandidateOps.
Provides common utility functions used across the application.
"""


import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union
import unicodedata


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a string to be used as a filename.
    Removes or replaces characters that are invalid in filenames.

    Args:
        filename: The filename to sanitize.
        max_length: Maximum length for the filename (default: 255).

    Returns:
        Sanitized filename safe for use in filesystems.
    """
    # Remove or replace invalid characters
    # Keep letters, numbers, spaces, and a few safe punctuation marks
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)

    # Remove control characters and normalize unicode
    sanitized = ''.join(
        char for char in sanitized
        if unicodedata.category(char)[0] != 'C'
    )

    # Replace multiple spaces/underscores with single underscore
    sanitized = re.sub(r'[\s_]+', '_', sanitized)

    # Remove leading/trailing whitespace and underscores
    sanitized = sanitized.strip(' _')

    # Ensure not empty
    if not sanitized:
        sanitized = "unnamed_file"

    # Truncate if too long
    if len(sanitized) > max_length:
        # Try to keep file extension if present
        if '.' in sanitized and max_length > 4:
            name_part, ext_part = sanitized.rsplit('.', 1)
            if len(ext_part) <= 10:  # Reasonable extension length
                available_length = max_length - len(ext_part) - 1
                if available_length > 0:
                    sanitized = f"{name_part[:available_length]}.{ext_part}"
                else:
                    sanitized = sanitized[:max_length]
            else:
                sanitized = sanitized[:max_length]
        else:
            sanitized = sanitized[:max_length]

    return sanitized


def generate_file_hash(file_path: Union[str, Path]) -> str:
    """
    Generate SHA256 hash of a file.

    Args:
        file_path: Path to the file.

    Returns:
        Hexadecimal SHA256 hash string.

    Raises:
        FileOperationError: If file cannot be read.
    """
    try:
        path = Path(file_path)
        if not path.is_file():
            raise FileOperationError(f"File not found: {file_path}")

        hash_sha256 = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()
    except Exception as e:
        raise FileOperationError(f"Failed to generate hash for {file_path}: {str(e)}")


def is_valid_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate.

    Returns:
        True if email format is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def parse_date_string(date_str: str, formats: Optional[List[str]] = None) -> Optional[datetime]:
    """
    Parse a date string using multiple possible formats.

    Args:
        date_str: Date string to parse.
        formats: List of date formats to try. If None, uses common formats.

    Returns:
        Parsed datetime object or None if parsing fails.
    """
    if formats is None:
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%b %d, %Y",
            "%d %b %Y"
        ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes.

    Returns:
        Formatted string (e.g., "1.5 MB").
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def ensure_directory_exists(directory_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory.

    Returns:
        Path object for the directory.

    Raises:
        FileOperationError: If directory cannot be created or accessed.
    """
    try:
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise FileOperationError(f"Failed to ensure directory exists {directory_path}: {str(e)}")


def chunk_list(items: List, chunk_size: int) -> List[List]:
    """
    Split a list into chunks of specified size.

    Args:
        items: List to split.
        chunk_size: Size of each chunk.

    Returns:
        List of lists where each inner list is a chunk.
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")

    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to maximum length with optional suffix.

    Args:
        text: String to truncate.
        max_length: Maximum length including suffix.
        suffix: String to append when truncating (default: "...").

    Returns:
        Truncated string.
    """
    if len(text) <= max_length:
        return text

    if len(suffix) >= max_length:
        return suffix[:max_length]

    return text[:max_length - len(suffix)] + suffix