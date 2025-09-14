from pydantic import BaseModel, Field
from ...domain.entities import Answer
from ..use_cases.answer_questions_use_case import AnswerQuestionUseCase

class ChatRequest(BaseModel):
    """Framework-agnostic request DTO serializable by delivery layer."""
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    """Structured response for delivery layer."""
    answer: str
    highlights: list[str]
    follow_up_questions: list[str]

class ChatController:
    """Thin coordination layer between delivery and use case.
    - translates request DTO -> use case call
    - translates domain Answer -> response DTO
    - no knowledge of FastAPI / HTTP specifics
    """
    def __init__(self, use_case: AnswerQuestionUseCase):
        self.use_case = use_case

    def handle(self, req: ChatRequest) -> ChatResponse:
        answer: Answer = self.use_case.execute(req.message)
        return ChatResponse(
            answer=answer.answer,
            highlights=answer.highlights,
            follow_up_questions=answer.follow_up_questions,
        )
