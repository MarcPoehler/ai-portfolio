from ...domain.ports.profile_repository import ProfileRepository
from ...domain.ports.llm_service import LLMService
from ...domain.entities import Answer, PIIFinding
from ...domain.errors import ValidationError, PIIBlockedError
from ...config import Settings
from ...application.suggestions.select_follow_up_questions import select_follow_up_questions
from .pii_processing_use_case import PIIProcessingUseCase

class AnswerQuestionUseCase:
    """Core orchestration:
    1) Load profile context
    2) Run optional PII processing
    3) Call LLM
    4) Attach follow-up questions
    """

    def __init__(
        self,
        profile_repository: ProfileRepository,
        llm_service: LLMService,
        settings: Settings | None = None,
        pii_processor: PIIProcessingUseCase | None = None,
    ):
        self.profile_repository = profile_repository
        self.llm_service = llm_service
        self.settings = settings
        self.pii_processor = pii_processor

    def execute(self, message: str) -> Answer:
        if not message or not message.strip():
            raise ValidationError("message must not be empty")
        if len(message) > 4000:
            raise ValidationError("message too long (max 4000 chars)")
        context_md = self.profile_repository.get_profile_text()

        # PII processing delegation
        if self.pii_processor:
            message, context_md = self.pii_processor.process(message, context_md)

        answer = self.llm_service.answer(prompt=message, context_markdown=context_md)

        try:
            count = self.settings.follow_up_questions_count if self.settings else 3
        except Exception:
            count = 3
        answer.follow_up_questions = select_follow_up_questions(
            current_question=message,
            answer=answer.answer,
            number_of_questions=count,
            exclude_ids=[],
        )
        return answer
