from typing import Protocol, List
from ..entities import PIIFinding

class PIIDetector(Protocol):
    """Outbound port for PII detection (swappable implementation)."""
    def detect(self, text: str) -> List[PIIFinding]: ...
