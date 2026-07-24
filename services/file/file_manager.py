"""
File management module for CandidateOps.
Handles creating candidate folders and downloading attachments from SAP.
"""


from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Dict, Any
import shutil
import mimetypes
from urllib.parse import urljoin, urlparse

from models.candidate import Candidate
from utils.exceptions import FileOperationError
from utils.logging_setup import get_logger
from utils.helpers import sanitize_filename, ensure_directory_exists
from infrastructure.config.settings import settings


logger = get_logger(__name__)


class FileManager:
    """
    Manages file system operations for candidate data.
    """

    def __init__(self, base_output_dir: Optional[Path] = None):
        """
        Initialize file manager.

        Args:
            base_output_dir: Base directory for storing candidate data.
        """
        self.base_output_dir = base_output_dir or settings.file.base_output_dir
        self.attachments_dir_name = settings.file.attachments_dir
        self.max_filename_length = settings.file.max_filename_length

        # Ensure base directory exists
        ensure_directory_exists(self.base_output_dir)
        logger.info(f"File manager initialized with base directory: {self.base_output_dir}")

    def create_candidate_folder(self, candidate: Candidate) -> Path:
        """
        Create a folder for a candidate based on their name and ID.

        Args:
            candidate: Candidate object.

        Returns:
            Path to the created candidate folder.

        Raises:
            FileOperationError: If folder cannot be created.
        """
        try:
            # Create folder name: "FirstName_LastName_ID" or similar
            safe_name = sanitize_filename(candidate.name, max_length=100)
            folder_name = f"{safe_name}_{candidate.candidate_id}"
            folder_name = sanitize_filename(folder_name, max_length=self.max_filename_length)

            candidate_folder = self.base_output_dir / folder_name
            ensure_directory_exists(candidate_folder)

            # Create attachments subfolder
            attachments_folder = candidate_folder / self.attachments_dir_name
            ensure_directory_exists(attachments_folder)

            logger.info(f"Created candidate folder: {candidate_folder}")
            return candidate_folder

        except Exception as e:
            logger.error(f"Failed to create candidate folder for {candidate.candidate_id}: {str(e)}")
            raise FileOperationError(f"Failed to create candidate folder: {str(e)}")

    def save_resume(self, candidate: Candidate, resume_content: bytes,
                   filename: Optional[str] = None) -> Path:
        """
        Save resume/CV file for a candidate.

        Args:
            candidate: Candidate object.
            resume_content: Binary content of the resume file.
            filename: Optional filename. If None, generates based on candidate name.

        Returns:
            Path to the saved resume file.

        Raises:
            FileOperationError: If file cannot be saved.
        """
        try:
            candidate_folder = self.create_candidate_folder(candidate)

            # Determine filename
            if filename is None:
                safe_name = sanitize_filename(candidate.name)
                filename = f"{safe_name}_Resume.pdf"
            else:
                filename = sanitize_filename(filename, max_length=self.max_filename_length)

            # Ensure PDF extension if not provided
            if not filename.lower().endswith(('.pdf', '.doc', '.docx')):
                filename += '.pdf'

            resume_path = candidate_folder / filename

            # Write file
            with resume_path.open('wb') as f:
                f.write(resume_content)

            logger.info(f"Saved resume for candidate {candidate.candidate_id} to {resume_path}")
            return resume_path

        except Exception as e:
            logger.error(f"Failed to save resume for candidate {candidate.candidate_id}: {str(e)}")
            raise FileOperationError(f"Failed to save resume: {str(e)}")

    def save_cover_letter(self, candidate: Candidate, cover_letter_content: bytes,
                         filename: Optional[str] = None) -> Path:
        """
        Save cover letter file for a candidate.

        Args:
            candidate: Candidate object.
            cover_letter_content: Binary content of the cover letter.
            filename: Optional filename. If None, generates based on candidate name.

        Returns:
            Path to the saved cover letter file.

        Raises:
            FileOperationError: If file cannot be saved.
        """
        try:
            candidate_folder = self.create_candidate_folder(candidate)

            # Determine filename
            if filename is None:
                safe_name = sanitize_filename(candidate.name)
                filename = f"{safe_name}_CoverLetter.pdf"
            else:
                filename = sanitize_filename(filename, max_length=self.max_filename_length)

            # Ensure PDF extension if not provided
            if not filename.lower().endswith(('.pdf', '.doc', '.docx')):
                filename += '.pdf'

            cover_letter_path = candidate_folder / filename

            # Write file
            with cover_letter_path.open('wb') as f:
                f.write(cover_letter_content)

            logger.info(f"Saved cover letter for candidate {candidate.candidate_id} to {cover_letter_path}")
            return cover_letter_path

        except Exception as e:
            logger.error(f"Failed to save cover letter for candidate {candidate.candidate_id}: {str(e)}")
            raise FileOperationError(f"Failed to save cover letter: {str(e)}")

    def save_attachment(self, candidate: Candidate, attachment_content: bytes,
                       filename: str, attachment_type: str = "general") -> Path:
        """
        Save a generic attachment file for a candidate.

        Args:
            candidate: Candidate object.
            attachment_content: Binary content of the attachment.
            filename: Original filename of the attachment.
            attachment_type: Type of attachment (for categorization).

        Returns:
            Path to the saved attachment file.

        Raises:
            FileOperationError: If file cannot be saved.
        """
        try:
            candidate_folder = self.create_candidate_folder(candidate)
            attachments_folder = candidate_folder / self.attachments_dir_name
            ensure_directory_exists(attachments_folder)

            # Sanitize filename
            safe_filename = sanitize_filename(filename, max_length=self.max_filename_length)
            if not safe_filename:
                safe_filename = f"attachment_{attachment_type}"

            # Avoid filename conflicts by adding counter if needed
            attachment_path = attachments_folder / safe_filename
            counter = 1
            original_path = attachment_path
            while attachment_path.exists():
                stem = original_path.stem
                suffix = original_path.suffix
                attachment_path = attachments_folder / f"{stem}_{counter}{suffix}"
                counter += 1

            # Write file
            with attachment_path.open('wb') as f:
                f.write(attachment_content)

            logger.info(f"Saved attachment for candidate {candidate.candidate_id}: {attachment_path}")
            return attachment_path

        except Exception as e:
            logger.error(f"Failed to save attachment for candidate {candidate.candidate_id}: {str(e)}")
            raise FileOperationError(f"Failed to save attachment: {str(e)}")

    def download_file_from_url(self, url: str, session_cookies: Optional[Dict[str, str]] = None,
                              headers: Optional[Dict[str, str]] = None) -> bytes:
        """
        Download file content from a URL (placeholder for actual implementation).

        Args:
            url: URL to download from.
            session_cookies: Optional cookies for authentication.
            headers: Optional HTTP headers.

        Returns:
            Binary content of the downloaded file.

        Note:
            This is a placeholder implementation. In a real scenario, this would use
            requests or similar library with proper session handling for SAP.
        """
        # Placeholder implementation - in real implementation, this would use:
        # import requests
        # response = requests.get(url, cookies=session_cookies, headers=headers)
        # response.raise_for_status()
        # return response.content

        logger.warning(f"Download from URL not implemented: {url}")
        # Return dummy content for demonstration
        return b"Dummy file content for demonstration purposes"

    def get_candidate_folder_path(self, candidate: Candidate) -> Path:
        """
        Get the folder path for a candidate (creates if doesn't exist).

        Args:
            candidate: Candidate object.

        Returns:
            Path to the candidate's folder.
        """
        return self.create_candidate_folder(candidate)

    def list_candidate_attachments(self, candidate: Candidate) -> List[Path]:
        """
        List all attachment files for a candidate.

        Args:
            candidate: Candidate object.

        Returns:
            List of paths to attachment files.
        """
        try:
            candidate_folder = self.get_candidate_folder_path(candidate)
            attachments_folder = candidate_folder / self.attachments_dir_name

            if not attachments_folder.exists():
                return []

            # Return all files in attachments folder
            return [f for f in attachments_folder.iterdir() if f.is_file()]

        except Exception as e:
            logger.error(f"Failed to list attachments for candidate {candidate.candidate_id}: {str(e)}")
            return []

    def clean_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean temporary files older than specified age.

        Args:
            max_age_hours: Maximum age in hours for files to keep.

        Returns:
            Number of files cleaned.
        """
        # Placeholder implementation
        logger.info(f"Cleaning temp files older than {max_age_hours} hours")
        return 0