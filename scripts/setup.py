"""
Setup script for CandidateOps.
Helps with initial setup and configuration.
"""


import os
import shutil
from pathlib import Path


def setup_directories():
    """Create necessary directories for CandidateOps."""
    directories = [
        "templates",
        "output",
        "candidates_data",
        "logs",
        "config",
        "docs",
        "tests/unit",
        "tests/integration",
        "scripts",
        "assets"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")


def create_sample_template():
    """Create a sample Excel template file."""
    try:
        import pandas as pd

        # Create sample data with column headers
        sample_data = pd.DataFrame(columns=[
            "CandidateID", "Name", "Email", "Phone", "City", "CurrentPosition",
            "YearsExperience", "Education", "Skills", "ApplicationDate", "Status",
            "ResumePath", "CoverLetterPath", "AttachmentsCount", "Notes"
        ])

        # Ensure templates directory exists
        Path("templates").mkdir(exist_ok=True)

        # Save sample template
        template_path = Path("templates/candidate_template.xlsx")
        sample_data.to_excel(template_path, index=False)
        print(f"Created sample Excel template: {template_path}")

    except ImportError:
        print("pandas not available, skipping sample template creation")
        print("Install pandas to generate sample templates: pip install pandas")


def create_env_example():
    """Create example environment file if it doesn't exist."""
    env_example = Path(".env.example")
    if not env_example.exists():
        shutil.copy("config/.env.example", ".env.example")
        print("Created .env.example file")
    else:
        print(".env.example already exists")


def main():
    """Main setup function."""
    print("=== CandidateOps Setup ===")
    print("Setting up directories and sample files...")

    setup_directories()
    create_sample_template()
    create_env_example()

    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("1. Copy .env.example to .env and configure your SAP credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the demo: python scripts/demo.py")
    print("4. Try a single cycle: python -m app.main --username test --single-cycle")
    print("5. Read README.md for full documentation")


if __name__ == "__main__":
    main()