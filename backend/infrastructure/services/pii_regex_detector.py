import re
from typing import List
from ...domain.entities import PIIFinding
from ...domain.ports.pii_detector import PIIDetector

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"\b\+?\d[\d ()-]{7,}\d\b")
_STREET = re.compile(r"\b\d{1,4}\s+[A-ZÄÖÜa-zäöüß]+(?:straße|str\.|Street|Road|Rd|Ave|Allee)\b")

_PATTERNS = [
    ("EMAIL", _EMAIL, "medium"),
    ("PHONE", _PHONE, "medium"),
    ("ADDRESS", _STREET, "medium"),
]

class RegexPIIDetector(PIIDetector):
    def detect(self, text: str) -> List[PIIFinding]:
        findings: List[PIIFinding] = []
        for category, pattern, severity in _PATTERNS:
            for m in pattern.finditer(text):
                findings.append(
                    PIIFinding(
                        category=category,
                        value=m.group(0),
                        start=m.start(),
                        end=m.end(),
                        severity=severity,
                    )
                )
        return findings
