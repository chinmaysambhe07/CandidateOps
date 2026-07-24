"""
Unit tests for Excel handler.
Tests ExcelHandler functionality for reading and writing candidate data.
"""


import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from services.excel.excel_handler import ExcelHandler
from models.candidate import Candidate
from utils.exceptions import ExcelError


def test_excel_handler_initialization():
    """Test ExcelHandler initialization."""
    handler = ExcelHandler()

    assert handler.template_path == Path("./templates/candidate_template.xlsx")
    assert handler.output_path == Path("./output/candidates_tracking.xlsx")
    assert handler.sheet_name == "Candidates"
    assert handler.id_column == "CandidateID"


def test_excel_handler_read_empty_file():
    """Test reading from non-existent Excel file returns empty list."""
    handler = ExcelHandler()

    # Mock file not existing
    with patch('pathlib.Path.exists', return_value=False):
        candidates = handler.read_candidates()
        assert candidates == []


def test_excel_handler_read_existing_file():
    """Test reading candidates from existing Excel file."""
    # Sample data
    sample_data = pd.DataFrame([
        {
            "CandidateID": "CAND001",
            "Name": "John Doe",
            "Email": "john.doe@email.com",
            "Phone": "+1-555-0123",
            "City": "New York",
            "CurrentPosition": "Software Engineer",
            "YearsExperience": 4,
            "Education": "Bachelor's in Computer Science",
            "Skills": "Python, Java",
            "ApplicationDate": "2024-01-15",
            "Status": "Applied",
            "ResumePath": "",
            "CoverLetterPath": "",
            "AttachmentsCount": 0,
            "Notes": ""
        }
    ])

    handler = ExcelHandler()

    with patch('pandas.read_excel', return_value=sample_data):
        with patch('pathlib.Path.exists', return_value=True):
            candidates = handler.read_candidates()

            assert len(candidates) == 1
            assert candidates[0].candidate_id == "CAND001"
            assert candidates[0].name == "John Doe"
            assert candidates[0].email == "john.doe@email.com"
            assert candidates[0].years_experience == 4


def test_excel_handler_write_candidates():
    """Test writing candidates to Excel file."""
    handler = ExcelHandler()

    candidates = [
        Candidate(
            candidate_id="CAND001",
            name="John Doe",
            email="john.doe@email.com",
            years_experience=3
        ),
        Candidate(
            candidate_id="CAND002",
            name="Jane Smith",
            email="jane.smith@email.com",
            years_experience=5
        )
    ]

    with patch('pandas.ExcelWriter') as mock_writer:
        mock_context = Mock()
        mock_writer.return_value.__enter__.return_value = mock_context

        handler.write_candidates(candidates)

        # Verify that to_excel was called
        mock_context.to_excel.assert_called_once()


def test_excel_handler_find_candidate_by_id():
    """Test finding candidate by ID."""
    handler = ExcelHandler()

    # Mock existing candidates
    existing_candidates = [
        Candidate(candidate_id="CAND001", name="John Doe"),
        Candidate(candidate_id="CAND002", name="Jane Smith")
    ]

    with patch.object(handler, 'read_candidates', return_value=existing_candidates):
        # Test finding existing candidate
        found = handler.find_candidate_by_id("CAND001")
        assert found is not None
        assert found.candidate_id == "CAND001"
        assert found.name == "John Doe"

        # Test finding non-existing candidate
        not_found = handler.find_candidate_by_id("CAND999")
        assert not_found is None


def test_excel_handler_add_candidate():
    """Test adding a new candidate."""
    handler = ExcelHandler()

    new_candidate = Candidate(candidate_id="CAND003", name="Bob Johnson")

    with patch.object(handler, 'read_candidates', return_value=[]):
        with patch.object(handler, 'write_candidates') as mock_write:
            handler.add_candidate(new_candidate)

            # Verify write_candidates was called with the new candidate
            mock_write.assert_called_once()
            args, _ = mock_write.call_args
            written_candidates = args[0]
            assert len(written_candidates) == 1
            assert written_candidates[0].candidate_id == "CAND003"


def test_excel_handler_add_duplicate_candidate():
    """Test adding duplicate candidate raises error."""
    handler = ExcelHandler()

    existing_candidate = Candidate(candidate_id="CAND001", name="John Doe")
    new_candidate = Candidate(candidate_id="CAND001", name="Johnny Doe")  # Same ID

    with patch.object(handler, 'read_candidates', return_value=[existing_candidate]):
        with pytest.raises(Exception):  # Should raise ExcelError or similar
            handler.add_candidate(new_candidate)


def test_excel_handler_update_candidate():
    """Test updating an existing candidate."""
    handler = ExcelHandler()

    updated_candidate = Candidate(
        candidate_id="CAND001",
        name="John Doe Updated",
        email="john.doe.updated@email.com"
    )

    existing_candidates = [
        Candidate(candidate_id="CAND001", name="John Doe"),
        Candidate(candidate_id="CAND002", name="Jane Smith")
    ]

    with patch.object(handler, 'read_candidates', return_value=existing_candidates):
        with patch.object(handler, 'write_candidates') as mock_write:
            result = handler.update_candidate(updated_candidate)

            assert result is True
            mock_write.assert_called_once()


def test_excel_handler_update_nonexistent_candidate():
    """Test updating non-existent candidate returns False."""
    handler = ExcelHandler()

    candidate = Candidate(candidate_id="CAND999", name="Non Existent")

    with patch.object(handler, 'read_candidates', return_value=[]):
        result = handler.update_candidate(candidate)
        assert result is False


def test_excel_handler_get_next_available_row():
    """Test getting next available row number."""
    handler = ExcelHandler()

    # Mock worksheet with existing data
    mock_worksheet = Mock()
    mock_worksheet.max_row = 5  # 4 data rows + 1 header
    handler.worksheet = mock_worksheet

    next_row = handler.get_next_available_row()
    assert next_row == 6  # Should be after the last row