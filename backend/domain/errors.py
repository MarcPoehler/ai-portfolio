class DomainError(Exception):
    """Base class for domain errors."""

class ValidationError(DomainError):
    """Invalid domain-level input (before technical/HTTP layer)."""

class NotFoundError(DomainError):
    """Expected domain data is missing (e.g., profile not found)."""

class PIIBlockedError(DomainError):
    """Raised when user input contains disallowed PII per policy."""
    def __init__(self, message: str, findings: list[dict]):
        super().__init__(message)
        self.findings = findings
