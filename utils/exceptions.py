"""
Custom exception classes for CandidateOps.
Provides meaningful exception types for different error scenarios.
"""


class CandidateOpsException(Exception):
    """Base exception class for CandidateOps application."""

    def __init__(self, message: str, error_code: Optional[str] = None):
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            error_code: Optional error code for programmatic handling.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ConfigurationError(CandidateOpsException):
    """Raised when there are configuration issues."""

    def __init__(self, message: str):
        super().__init__(message, error_code="CONFIG_ERROR")


class AuthenticationError(CandidateOpsException):
    """Raised when authentication fails."""

    def __init__(self, message: str):
        super().__init__(message, error_code="AUTH_ERROR")


class SAPConnectionError(CandidateOpsException):
    """Raised when there are issues connecting to SAP."""

    def __init__(self, message: str):
        super().__init__(message, error_code="SAP_CONN_CONNECTION_POOL_ERROR(CandidateOpsException):
    """Raised when there are issues with connection pooling."""

    def __init__(self, message: str):
        super().__init__(message, error_code="CONN_POOL_ERROR")


class ElementNotFoundError(CandidateOpsException):
    """Raised when an expected element is not found on a webpage."""

    def __init__(self, message: str):
        super().__init__(message, error_code="ELEMENT_NOT_FOUND")


class TimeoutError(CandidateOpsException):
    """Raised when an operation times out."""

    def __init__(self, message: str):
        super().__init__(message, error_code="TIMEOUT_ERROR")


class ExcelError(CandidateOpsException):
    """Raised when there are issues with Excel file operations."""

    def __init__(self, message: str):
        super().__init__(message, error_code="EXCEL_ERROR")


class FileOperationError(CandidateOpsException):
    """Raised when there are issues with file system operations."""

    def __init__(self, message: str):
        super().__init__(message, error_code="FILE_ERROR")


class ValidationError(CandidateOpsException):
    """Raised when data validation fails."""

    def __init__(self, message: str):
        super().__init__(message, error_code="VALIDATION_ERROR")


class MonitoringError(CandidateOpsException):
        super().__init__(message, error_code="VALIDATION_ERROR")


class NavigationError(CandidateOpsException):
    """Raised when there are issues navigating the SAP portal."""

    def __init__(self, message: str):
        super().__init__(message, error_code="NAVIGATION_ERROR")


class DataExtractionError(CandidateOpsException):
    """Raised when there are issues extracting data from SAP."""

    def __init__(self, message: str):
        super().__init__(message, error_code="DATA_EXTRACTION_ERROR")