# CandidateOps Configuration Settings

"""
Configuration management for CandidateOps using Pydantic Settings.
Loads configuration from environment variables and config.yaml file.
"""

from pathlib import Path
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    url: str = Field(default="sqlite:///./candidate_ops.db", description="Database URL")
    echo: bool = Field(default=False, description="Echo SQL queries")


class SapSettings(BaseSettings):
    """SAP Career portal configuration."""
    base_url: str = Field(..., description="SAP Career portal base URL")
    login_endpoint: str = Field(default="/login", description="Login endpoint")
    career_endpoint: str = Field(default="/career", description="Career portal endpoint")
    timeout: int = Field(default=30, description="Page load timeout in seconds")
    implicit_wait: int = Field(default=10, description="Implicit wait time in seconds")

    @validator('base_url')
    def validate_base_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Base URL must start with http:// or https://')
        return v.rstrip('/')


class ExcelSettings(BaseSettings):
    """Excel file handling configuration."""
    template_path: Path = Field(default=Path("./templates/candidate_template.xlsx"),
                               description="Path to Excel template file")
    output_path: Path = Field(default=Path("./output/candidates_tracking.xlsx"),
                             description="Path for output Excel file")
    sheet_name: str = Field(default="Candidates", description="Excel sheet name")
    id_column: str = Field(default="CandidateID", description="Column name for candidate ID")


class FileSettings(BaseSettings):
    """File system operations configuration."""
    base_output_dir: Path = Field(default=Path("./candidates_data"),
                                 description="Base directory for candidate data")
    attachments_dir: str = Field(default="attachments",
                                description="Subdirectory for attachments")
    max_filename_length: int = Field(default=255,
                                    description="Maximum filename length")


class LoggingSettings(BaseSettings):
    """Logging configuration."""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date format for logs"
    )
    console_enabled: bool = Field(default=True, description="Enable console logging")
    file_enabled: bool = Field(default=True, description="Enable file logging")
    file_path: Path = Field(default=Path("./logs/candidate_ops.log"),
                           description="Log file path")
    max_bytes: int = Field(default=10*1024*1024,  # 10 MB
                          description="Maximum size of log file before rotation")
    backup_count: int = Field(default=5,
                             description="Number of backup log files to keep")


class MonitoringSettings(BaseSettings):
    """Application monitoring configuration."""
    check_interval: int = Field(default=300,  # 5 minutes
                               description="Interval between checks in seconds")
    max_runtime_hours: int = Field(default=8,
                                  description="Maximum runtime before auto-stop")
    enable_notifications: bool = Field(default=False,
                                      description="Enable completion notifications")


class Settings(BaseSettings):
    """Main application settings combining all configuration sections."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        yaml_file="config/config.yaml"
    )

    # Application info
    app_name: str = Field(default="CandidateOps", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Nested configuration sections
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    sap: SapSettings = Field(default_factory=SapSettings)
    excel: ExcelSettings = Field(default_factory=ExcelSettings)
    file: FileSettings = Field(default_factory=FileSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)

    @validator('sap')
    def validate_sap_settings(cls, v):
        """Validate SAP settings are not using default placeholder values."""
        if v.base_url == "https://example.com/sap":
            raise ValueError(
                "SAP base_url must be configured. Please set SAP__BASE_URL in .env or config.yaml"
            )
        return v


# Global settings instance
settings = Settings()