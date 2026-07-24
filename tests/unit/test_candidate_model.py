"""
Unit tests for Candidate data model.
Tests the Candidate model functionality including validation, serialization, and helper methods.
"""


import pytest
from datetime import datetime
from pathlib import Path

from models.candidate import Candidate


def test_candidate_creation_valid():
    """Test creating a valid candidate."""
    candidate = Candidate(
        candidate_id="CAND001",
        name="John Doe",
        email="john.doe@email.com",
        phone="+1-555-0123",
        city="New York",
        current_position="Software Engineer",
        years_experience=4,
        education="Bachelor's in Computer Science",
        skills=["Python", "Java"],
        application_date=datetime(2024, 1, 15),
        status="Applied"
    )

    assert candidate.candidate_id == "CAND001"
    assert candidate.name == "John Doe"
    assert candidate.email == "john.doe@email.com"
    assert candidate.years_experience == 4
    assert candidate.skills == ["Python", "Java"]


def test_candidate_creation_minimal():
    """Test creating a candidate with minimal required fields."""
    candidate = Candidate(candidate_id="CAND002")

    assert candidate.candidate_id == "CAND002"
    assert candidate.name == ""
    assert candidate.email == ""
    assert candidate.years_experience == 0
    assert candidate.skills == []
    assert candidate.status == "New"


def test_candidate_invalid_email():
    """Test that invalid email raises ValueError."""
    with pytest.raises(ValueError, match="Invalid email format"):
        Candidate(
            candidate_id="CAND003",
            name="Jane Doe",
            email="invalid-email",
            candidate_id="CAND003"
        )


def test_candidate_negative_experience():
    """Test that negative years experience raises ValueError."""
    with pytest.raises(ValueError, match="Years of experience cannot be negative"):
        Candidate(
            candidate_id="CAND004",
            name="Bob Smith",
            years_experience=-1
        )


def test_candidate_to_dict():
    """Test converting candidate to dictionary."""
    candidate = Candidate(
        candidate_id="CAND005",
        name="Alice Johnson",
        email="alice@email.com",
        phone="+1-555-0456",
        city="San Francisco",
        current_position="Data Scientist",
        years_experience=3,
        education="Master's in Statistics",
        skills=["Python", "R", "SQL"],
        application_date=datetime(2024, 1, 10),
        status="Applied",
        notes="Strong analytical background"
    )

    candidate_dict = candidate.to_dict()

    assert candidate_dict["CandidateID"] == "CAND005"
    assert candidate_dict["Name"] == "Alice Johnson"
    assert candidate_dict["Email"] == "alice@email.com"
    assert candidate_dict["YearsExperience"] == 3
    assert candidate_dict["Skills"] == "Python, R, SQL"
    assert candidate_dict["Status"] == "Applied"
    assert candidate_dict["Notes"] == "Strong analytical background"


def test_candidate_from_dict():
    """Test creating candidate from dictionary."""
    data = {
        "CandidateID": "CAND006",
        "Name": "Tom Wilson",
        "Email": "tom@email.com",
        "Phone": "+1-555-0789",
        "City": "Boston",
        "CurrentPosition": "DevOps Engineer",
        "YearsExperience": 5,
        "Education": "Bachelor's in Engineering",
        "Skills": "AWS, Docker, Kubernetes",
        "ApplicationDate": "2024-01-12",
        "Status": "Applied",
        "Notes": "Cloud infrastructure expert",
        "ResumePath": "",
        "CoverLetterPath": "",
        "AttachmentsCount": 0
    }

    candidate = Candidate.from_dict(data)

    assert candidate.candidate_id == "CAND006"
    assert candidate.name == "Tom Wilson"
    assert candidate.email == "tom@email.com"
    assert candidate.years_experience == 5
    assert candidate.skills == ["AWS", "Docker", "Kubernetes"]
    assert candidate.application_date == datetime(2024, 1, 12)
    assert candidate.status == "Applied"
    assert candidate.notes == "Cloud infrastructure expert"


def test_candidate_has_resume():
    """Test checking if candidate has resume."""
    candidate = Candidate(candidate_id="CAND007")

    # Initially no resume
    assert not candidate.has_resume()

    # Set resume path
    candidate.resume_path = Path("/tmp/resume.pdf")
    assert candidate.has_resume()


def test_candidate_get_attachment_count():
    """Test getting attachment count."""
    candidate = Candidate(candidate_id="CAND008")

    # Initially no attachments
    assert candidate.get_attachment_count() == 0

    # Add resume
    candidate.resume_path = Path("/tmp/resume.pdf")
    assert candidate.get_attachment_count() == 1

    # Add cover letter
    candidate.cover_letter_path = Path("/tmp/cover_letter.pdf")
    assert candidate.get_attachment_count() == 2

    # Add additional attachment
    candidate.additional_attachments = [Path("/tmp/transcript.pdf")]
    assert candidate.get_attachment_count() == 3


def test_candidate_get_full_name():
    """Test getting full name."""
    candidate = Candidate(candidate_id="CAND009", name="  John  Doe  ")
    assert candidate.get_full_name() == "John Doe"

    candidate_empty = Candidate(candidate_id="CAND010")
    assert candidate_empty.get_full_name() == ""