"""
Data models for CandidateOps.
Defines the core data structures used throughout the application.
"""


from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import re


@dataclass
class Candidate:
    """
    Represents a candidate in the recruitment system.

    Attributes:
        candidate_id: Unique identifier for the candidate (from SAP)
        name: Full name of the candidate
        email: Email address
        phone: Phone number
        city: City of residence
        current_position: Current job title/position
        years_experience: Years of professional experience
        education: Highest education level
        skills: List of technical/soft skills
        application_date: Date when candidate applied
        status: Current application status
        resume_path: Local path to downloaded resume/CV
        cover_letter_path: Local path to downloaded cover letter
        additional_attachments: List of paths to other attachments
        notes: Any additional notes about the candidate
    """

    candidate_id: str
    name: str = ""
    email: str = ""
    phone: str = ""
    city: str = ""
    current_position: str = ""
    years_experience: int = 0
    education: str = ""
    skills: List[str] = field(default_factory=list)
    application_date: Optional[datetime] = None
    status: str = "New"
    resume_path: Optional[Path] = None
    cover_letter_path: Optional[Path] = None
    additional_attachments: List[Path] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self) -> None:
        """Validate candidate data after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate candidate fields."""
        if not self.candidate_id:
            raise ValueError("Candidate ID is required")

        if self.email and not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")

        if self.years_experience < 0:
            raise ValueError("Years of experience cannot be negative")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def get_full_name(self) -> str:
        """Get the candidate's full name."""
        return self.name.strip()

    def has_resume(self) -> bool:
        """Check if candidate has a resume file."""
        return self.resume_path is not None and self.resume_path.exists()

    def get_attachment_count(self) -> int:
        """Get total number of attachments."""
        count = 0
        if self.resume_path and self.resume_path.exists():
            count += 1
        if self.cover_letter_path and self.cover_letter_path.exists():
            count += 1
        count += sum(1 for path in self.additional_attachments if path.exists())
        return count

    def to_dict(self) -> dict:
        """
        Convert candidate to dictionary for Excel export.

        Returns:
            Dictionary representation of the candidate.
        """
        return {
            "CandidateID": self.candidate_id,
            "Name": self.name,
            "Email": self.email,
            "Phone": self.phone,
            "City": self.city,
            "CurrentPosition": self.current_position,
            "YearsExperience": self.years_experience,
            "Education": self.education,
            "Skills": ", ".join(self.skills),
            "ApplicationDate": self.application_date.strftime("%Y-%m-%d") if self.application_date else "",
            "Status": self.status,
            "ResumePath": str(self.resume_path) if self.resume_path else "",
            "CoverLetterPath": str(self.cover_letter_path) if self.cover_letter_path else "",
            "AttachmentsCount": self.get_attachment_count(),
            "Notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> Candidate:
        """
        Create Candidate instance from dictionary (e.g., from Excel row).

        Args:
            data: Dictionary containing candidate data.

        Returns:
            Candidate instance.
        """
        # Parse application date if present
        application_date = None
        if data.get("ApplicationDate"):
            try:
                application_date = datetime.strptime(data["ApplicationDate"], "%Y-%m-%d")
            except ValueError:
                pass  # Keep as None if parsing fails

        # Parse skills if present
        skills = []
        if data.get("Skills"):
            skills = [skill.strip() for skill in data["Skills"].split(",") if skill.strip()]

        return cls(
            candidate_id=str(data.get("CandidateID", "")),
            name=str(data.get("Name", "")),
            email=str(data.get("Email", "")),
            phone=str(data.get("Phone", "")),
            city=str(data.get("City", "")),
            current_position=str(data.get("CurrentPosition", "")),
            years_experience=int(data.get("YearsExperience", 0)) if data.get("YearsExperience") else 0,
            education=str(data.get("Education", "")),
            skills=skills,
            application_date=application_date,
            status=str(data.get("Status", "New")),
            notes=str(data.get("Notes", ""))
        )


@dataclass
class Position:
    """
    Represents a job position in the SAP system.

    Attributes:
        position_id: Unique identifier for the position
        title: Job title
        department: Department name
        location: Job location
        description: Job description
        requirements: Job requirements
        url: Direct URL to the position in SAP
        active: Whether the position is currently active/open
    """

    position_id: str
    title: str = ""
    department: str = ""
    location: str = ""
    description: str = ""
    requirements: str = ""
    url: str = ""
    active: bool = True

    def __post_init__(self) -> None:
        """Validate position data after initialization."""
        if not self.position_id:
            raise ValueError("Position ID is required")

    def is_active(self) -> bool:
        """Check if position is active."""
        return self.active

    def get_display_name(self) -> str:
        """Get formatted display name for the position."""
        parts = [self.title]
        if self.department:
            parts.append(f"({self.department})")
        if self.location:
            parts.append(f"- {self.location}")
        return " ".join(parts)


@dataclass
class Application:
    """
    Represents a job application in the system.

    Attributes:
        application_id: Unique identifier for the application
        candidate: Candidate who applied
        position: Position applied for
        applied_at: Timestamp when application was submitted
        source: How the candidate found the position (e.g., company website, job board)
        cover_letter: Text of cover letter if provided
        status: Current status of the application
    """

    application_id: str
    candidate: Candidate
    position: Position
    applied_at: datetime = field(default_factory=datetime.now)
    source: str = ""
    cover_letter: str = ""
    status: str = "Submitted"

    def __post_init__(self) -> None:
        """Validate application data after initialization."""
        if not self.application_id:
            raise ValueError("Application ID is required")
        if not self.candidate.candidate_id:
            raise ValueError("Candidate ID is required")
        if not self.position.position_id:
            raise ValueError("Position ID is required")

    def is_recent(self, hours: int = 24) -> bool:
        """
        Check if application was submitted within last N hours.

        Args:
            hours: Number of hours to check against.

        Returns:
            True if application is recent, False otherwise.
        """
        delta = datetime.now() - self.applied_at
        return delta.total_seconds() < (hours * 3600)