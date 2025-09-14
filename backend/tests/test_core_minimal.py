import pytest
from backend.application.use_cases.answer_questions_use_case import AnswerQuestionUseCase
from backend.application.use_cases.pii_processing_use_case import PIIProcessingUseCase
from backend.domain.entities import Answer, PIIFinding
from backend.domain.errors import ValidationError, PIIBlockedError
from backend.config import Settings

# Test Doubles

class DummyProfileRepo:
    def __init__(self):
        self.calls = 0
    def get_profile_text(self) -> str:  
        self.calls += 1
        return "Profile Background"

class DummyLLM:
    def answer(self, prompt: str, context_markdown: str) -> Answer:
        return Answer(answer=f"Echo: {prompt}", highlights=["h"], follow_up_questions=[])

class DummyPII:
    def __init__(self, findings):
        self._findings = findings
    def detect(self, text: str):
        return self._findings

# Tests

def test_validation_empty():
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM())
    with pytest.raises(ValidationError):
        uc.execute("")


def test_max_length():
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM())
    long_msg = "x" * 4001
    with pytest.raises(ValidationError):
        uc.execute(long_msg)


def test_basic_flow_two_calls():
    repo = DummyProfileRepo()
    uc = AnswerQuestionUseCase(repo, DummyLLM())
    ans1 = uc.execute("Hello")
    ans2 = uc.execute("World")
    assert ans1.answer.startswith("Echo:")
    assert ans2.answer.startswith("Echo:")
    assert repo.calls == 2


def test_pii_block():
    settings = Settings()
    settings.pii_enabled = True
    settings.pii_block_severity = "low"
    detector = DummyPII([PIIFinding(category="EMAIL", value="a@b.com", start=0, end=6, severity="high")])
    pii_proc = PIIProcessingUseCase(detector, settings)
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM(), settings=settings, pii_processor=pii_proc)
    with pytest.raises(PIIBlockedError):
        uc.execute("a@b.com please answer")


def test_pii_mask():
    settings = Settings()
    settings.pii_enabled = True
    settings.pii_block_severity = "high"
    detector = DummyPII([PIIFinding(category="PHONE", value="+123", start=0, end=5, severity="medium")])
    pii_proc = PIIProcessingUseCase(detector, settings)
    uc = AnswerQuestionUseCase(DummyProfileRepo(), DummyLLM(), settings=settings, pii_processor=pii_proc)
    ans = uc.execute("+123 rest")
    assert "PHONE_" in ans.answer
