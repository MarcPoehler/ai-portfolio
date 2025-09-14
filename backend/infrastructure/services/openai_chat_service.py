import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from pydantic import ValidationError

from ...domain.ports.llm_service import LLMService
from ...domain.entities import Answer


class OpenAIChatService(LLMService):
    """Minimal OpenAI Chat Completions based implementation.

    Tool calling and direct profile read support were removed for demo simplicity.
    """

    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


    # Public API (Port)
    def answer(self, prompt: str, context_markdown: str) -> Answer:
        """Generate an answer enforcing JSON output with required keys.

        Strategy (Option A):
        - Use response_format JSON mode (if supported by model) to coerce JSON.
        - Provide explicit schema instructions.
        - Validate & attempt one repair if invalid.
        """

        # Build schema description dynamically from the Answer model
        _ans_schema = Answer.model_json_schema()
        _schema_core = {
            "type": _ans_schema.get("type", "object"),
            "properties": _ans_schema.get("properties", {}),
            "required": _ans_schema.get("required", []),
        }
        schema_description = json.dumps(_schema_core, separators=(",", ":"))


        system = (
            f"""System: You are an assistant specializing in answering questions specifically about a job candidate's qualifications, experience, and fit for a particular role within AI-focused companies (e.g., AI Engineers, AI Software Engineers).

            Your output MUST strictly follow this schema: {schema_description}

            Guidelines:
            - Respond ONLY with a valid JSON object. No markdown, no code fences, no explanations outside JSON.
            - The "answer" should sound natural and human, as if the candidate is speaking directly, but remain concise (2–4 sentences).
            - Always write the "answer" in first-person singular ("I") perspective of the candidate (e.g., "I live in Germany", "I worked on AI systems"). Never use third-person references like "the candidate", "he", "she".
            - "highlights" should emphasize remarkable achievements, distinctive skills, or unusual aspects that strengthen the answer. They must not be verbatim repeats of the "answer". There is no highlight needed for factual information.
            - Set "follow_up_questions" to an empty array []; it will be populated by the system after your response.
            - If information is unavailable, set "answer" to "Unknown" and leave "highlights" empty.
            - Always provide arrays, even if empty.
            - Ensure output is valid JSON (parsable, no trailing commas).
            - Use English only.
            - Do not invent information; only rely on the candidate’s knowledge base.
            - If multiple possible interpretations exist, choose the most relevant to AI/Software Engineering context.
            """
        )

        user_content = (
            f"Context (Markdown):\n{context_markdown}\n\nQuestion:\n{prompt}\n\nReturn ONLY a JSON object matching the schema."
        )

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type(Exception),
            reraise=True,
        )
        def _call(messages: List[Dict[str, Any]]):  # noqa: ANN202
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
            )

        response = _call(messages)
        raw = response.choices[0].message.content or ""
        try:
            answer_obj = Answer.model_validate_json(raw)
        except (json.JSONDecodeError, ValidationError):
            # Fallback: wrap raw text as answer
            answer_obj = Answer(answer=raw, highlights=[], follow_up_questions=[])
        return answer_obj
