from typing import Protocol
from ..entities import Answer


class LLMService(Protocol):
    """
    Outbound port: domain layer requests answers from an LLM.
    Concrete implementations live in the infrastructure layer (e.g., OpenAI Chat).
    """

    def answer(self, prompt: str, context_markdown: str) -> Answer:
        ...
