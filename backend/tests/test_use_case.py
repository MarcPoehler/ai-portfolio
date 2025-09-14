import pytest
from backend.application.use_cases.answer_questions_use_case import AnswerQuestionUseCase
from backend.application.use_cases.pii_processing_use_case import PIIProcessingUseCase
from backend.domain.entities import Answer, PIIFinding
from backend.domain.errors import ValidationError, PIIBlockedError
from backend.config import Settings

# Test Doubles

class DummyProfileRepo:
    def get_profile_text(self) -> str:
        return "Background text"

class DummyLLM:
    def answer(self, prompt: str, context_markdown: str) -> Answer:
        return Answer(answer=f"Echo: {prompt}", highlights=["h1"], follow_up_questions=[])

class DummyPII:
    def __init__(self, findings):
        self._findings = findings
    def detect(self, text: str):
        return self._findings


def test_empty_raises():
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM())
    with pytest.raises(ValidationError):
        uc.execute("")


def test_basic_flow():
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM())
    ans = uc.execute("Hello")
    assert ans.answer.startswith("Echo: Hello")
    assert ans.highlights


def test_pii_blocked():
    settings = Settings()
    settings.pii_enabled = True
    settings.pii_block_severity = "low"
    detector = DummyPII([PIIFinding(category="EMAIL", value="a@b.com", start=0, end=6, severity="high")])
    pii_proc = PIIProcessingUseCase(detector, settings)
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM(), settings=settings, pii_processor=pii_proc)
    with pytest.raises(PIIBlockedError):
        uc.execute("a@b.com question")


def test_pii_masking():
    settings = Settings()
    settings.pii_enabled = True
    settings.pii_block_severity = "high"
    detector = DummyPII([PIIFinding(category="PHONE", value="+123456789", start=0, end=10, severity="medium")])
    pii_proc = PIIProcessingUseCase(detector, settings)
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM(), settings=settings, pii_processor=pii_proc)
    ans = uc.execute("+123456789 tell me more")
    assert "PHONE_" in ans.answer
