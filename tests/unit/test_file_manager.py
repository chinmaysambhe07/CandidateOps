"""
Unit tests for File manager.
Tests FileManager functionality for file system operations.
"""


import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from services.file.file_manager import FileManager
from models.candidate import Candidate
from utils.exceptions import FileOperationError


def test_file_manager_initialization():
    """Test FileManager initialization."""
    fm = FileManager()

    assert fm.base_output_dir == Path("./candidates_data")
    assert fm.attachments_dir_name == "attachments"
    assert fm.max_filename_length == 255


def test_file_manager_initialization_custom_dir():
    """Test FileManager initialization with custom directory."""
    custom_dir = Path("/tmp/custom_candidates")
    fm = FileManager(base_output_dir=custom_dir)

    assert fm.base_output_dir == custom_dir
    assert fm.attachments_dir_name == "attachments"


def test_create_candidate_folder():
    """Test creating candidate folder."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "candidates"
        fm = FileManager(base_output_dir=base_dir)

        candidate = Candidate(
            candidate_id="CAND001",
            name="John Doe"
        )

        folder_path = fm.create_candidate_folder(candidate)

        # Check folder was created
        assert folder_path.exists()
        assert folder_path.is_dir()

        # Check folder name format
        assert "John_Doe_CAND001" in folder_path.name or "John_Doe" in folder_path.name

        # Check attachments subfolder exists
        attachments_folder = folder_path / "attachments"
        assert attachments_folder.exists()
        assert attachments_folder.is_dir()


def test_create_candidate_folder_sanitization():
    """Test that candidate folder creation sanitizes filenames."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "candidates"
        fm = FileManager(base_output_dir=base_dir)

        # Candidate with invalid filename characters
        candidate = Candidate(
            candidate_id="CAND001",
            name='John "Invalid/*Name" Doe'
        )

        folder_path = fm.create_candidate_folder(candidate)

        # Folder should exist and have sanitized name
        assert folder_path.exists()
        assert folder_path.is_dir()
        # Should not contain invalid characters
        assert '"' not in folder_path.name
        assert '*' not in folder_path.name
        assert '/' not in folder_path.name


def test_save_resume():
    """Test saving resume file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "candidates"
        fm = FileManager(base_output_dir=base_dir)

        candidate = Candidate(
            candidate_id="CAND001",
            name="Jane Smith"
        )

        resume_content = b"Fake PDF content for resume"
        saved_path = fm.save_resume(candidate, resume_content, "Jane_Smith_Resume.pdf")

        # Check file was created
        assert saved_path.exists()
        assert saved_path.is_file()

        # Check content
        with saved_path.open('rb') as f:
            content = f.read()
            assert content == resume_content

        # Check it's in the candidate's folder
        assert candidate.candidate_id in str(saved_path)
        assert "Resume" in saved_path.name


def test_save_cover_letter():
    """Test saving cover letter file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "candidates"
        fm = FileManager(base_output_dir=base_dir)

        candidate = Candidate(
            candidate_id="CAND002",
            name="Bob Johnson"
        )

        cover_letter_content = b"Fake PDF content for cover letter"
        saved_path = fm.save_cover_letter(candidate, cover_letter_content, "Bob_Cover.pdf")

        # Check file was created
        assert saved_path.exists()
        assert saved_path.is_file()

        # Check content
        with saved_path.open('rb') as f:
            content = f.read()
            assert content == cover_letter_content

        # Check it's in the candidate's folder and has correct name
        assert candidate.candidate_id in str(saved_path)
        assert "CoverLetter" in saved_path.name or "Cover" in saved_path.name


def test_save_attachment():
    """Test saving generic attachment."""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "candidates"
        fm = FileManager(base_output_dir=base_dir)

        candidate = Candidate(
            candidate_id="CAND003",
            name="Alice Williams"
        )

        attachment_content = b"Fake transcript content"
        saved_path = fm.save_attachment(candidate, attachment_content, "transcript.pdf", "transcript")

        # Check file was created
        assert saved_path.exists()
        assert saved_path.is_file()

        # Check content
        with saved_path.open('rb') as f:
            content = f.read()
            assert content == attachment_content

        # Check it's in the attachments subfolder
        assert "attachments" in str(saved_path)
        assert candidate.candidate_id in str(saved_path)
        assert "transcript" in saved_path.name


def test_sanitize_filename():
    """Test filename sanitization helper."""
    from utils.helpers import sanitize_filename

    # Test normal filename
    assert sanitize_filename("normal_file.pdf") == "normal_file.pdf"

    # Test filename with invalid characters
    assert sanitize_filename('file<>:/"\\|?*.pdf') == "file__________.pdf"

    # Test filename with spaces
    assert sanitize_filename("my file name.pdf") == "my_file_name.pdf"

    # Test empty filename
    assert sanitize_filename("") == "unnamed_file"

    # Test very long filename
    long_name = "a" * 300 + ".pdf"
    sanitized = sanitize_filename(long_name, max_length=100)
    assert len(sanitized) <= 100
    assert sanitized.endswith(".pdf")


def test_ensure_directory_exists():
    """Test ensure_directory_exists helper."""
    from utils.helpers import ensure_directory_exists

    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "new" / "nested" / "directory"

        # Directory doesn't exist yet
        assert not test_dir.exists()

        # Ensure it exists
        result_dir = ensure_directory_exists(test_dir)

        # Check it was created
        assert result_dir.exists()
        assert result_dir.is_dir()
        assert result_dir == test_dir

        # Calling again should not fail
        result_dir2 = ensure_directory_exists(test_dir)
        assert result_dir2 == test_dir


def test_generate_file_hash():
    """Test file hash generation helper."""
    from utils.helpers import generate_file_hash

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b"Hello, World!")
        tmp_file.flush()

        try:
            hash_value = generate_file_hash(tmp_file.name)
            # SHA256 of "Hello, World!"
            expected_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            assert hash_value == expected_hash
        finally:
            os.unlink(tmp_file.name)


def test_is_valid_email():
    """Test email validation helper."""
    from utils.helpers import is_valid_email

    # Valid emails
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("user.name@domain.co.uk") is True
    assert is_valid_email("user+tag@example.org") is True

    # Invalid emails
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("@example.com") is False
    assert is_valid_email("test@") is False
    assert is_valid_email("test@@example.com") is False


if __name__ == "__main__":
    pytest.main([__file__])