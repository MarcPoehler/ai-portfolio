from __future__ import annotations

from ...domain.entities import PIIFinding
from ...domain.errors import PIIBlockedError
from ...domain.ports.pii_detector import PIIDetector
from ...config import Settings


class PIIProcessingUseCase:
    """Encapsulates PII detection, blocking decision, and masking.

    Responsibilities:
    - Detect PII findings using an injected detector.
    - Decide if the request should be blocked based on severity threshold.
    - Optionally mask findings and augment context with a guidance note.

    Public contract:
        process(message, context_md) -> (sanitized_message, updated_context_md)
        May raise PIIBlockedError when policy requires blocking.
    """

    def __init__(self, detector: PIIDetector, settings: Settings):
        self.detector = detector
        self.settings = settings

    def _severity_rank(self, sev: str) -> int:
        order = {"low": 1, "medium": 2, "high": 3}
        return order.get(sev.lower(), 0)

    def _should_block(self, findings: list[PIIFinding]) -> bool:
        threshold = self._severity_rank(self.settings.pii_block_severity)
        if threshold <= 0:
            return False
        return any(self._severity_rank(f.severity) >= threshold for f in findings)

    def _mask(self, text: str, findings: list[PIIFinding]) -> str:
        if not findings:
            return text
        ordered = sorted(findings, key=lambda f: f.start)
        result: list[str] = []
        last = 0
        counts: dict[str, int] = {}
        for f in ordered:
            result.append(text[last:f.start])
            counts[f.category] = counts.get(f.category, 0) + 1
            token = f"<{f.category}_{counts[f.category]}>"
            result.append(token)
            last = f.end
        result.append(text[last:])
        return "".join(result)

    def process(self, message: str, context_md: str) -> tuple[str, str]:
        """Run detection, possibly block or mask.

        Returns a tuple of (possibly modified message, possibly augmented context).
        Raises PIIBlockedError if policy mandates blocking.
        """
        if not (self.settings.pii_enabled and self.detector):
            return message, context_md

        findings = self.detector.detect(message)
        if not findings:
            return message, context_md

        if self._should_block(findings):
            raise PIIBlockedError(
                "Input contains disallowed PII",
                [f.model_dump() for f in findings],
            )

        if self.settings.pii_mask:
            masked = self._mask(message, findings)
            note = (
                "NOTE: User input contained masked PII tokens like <EMAIL_1>. Do not attempt to guess originals.\n\n"
            )
            return masked, note + context_md
        return message, context_md
