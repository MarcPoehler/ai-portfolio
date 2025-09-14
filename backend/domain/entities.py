from pydantic import BaseModel, Field
from typing import Literal

Role = Literal["system", "user", "assistant"]

class ChatMessage(BaseModel):
    role: Role = Field(..., description="Role of the message sender")
    content: str = Field(..., min_length=1)

class Answer(BaseModel):
    answer: str = Field(..., min_length=1, description="Primary natural language answer")
    highlights: list[str] = Field(..., default_factory=list, description="Key bullet points summarizing the answer")
    follow_up_questions: list[str] = Field(..., default_factory=list, description="Suggested follow-up questions")

class PIIFinding(BaseModel):
    category: str = Field(..., description="Category of the PII finding")
    value: str = Field(..., description="The PII value found")
    start: int = Field(..., description="Start index of the PII finding in the input text")
    end: int = Field(..., description="End index of the PII finding in the input text")
    severity: str = Field(default="medium", description="Severity level of the PII finding")
