"""Selection logic for predefined follow-up questions.

1. Filter out excluded IDs.
2. Shuffle the remaining pool randomly.
3. Return first k texts.

Deliberately no relevance scoring – keeps it simple and predictable in complexity.
"""

from __future__ import annotations

from typing import List, Sequence
import random

from .follow_up_questions_catalog import QUESTIONS

def select_follow_up_questions(
    current_question: str,
    answer: str,  # bleibt vorhanden für API-Kompatibilität
    number_of_questions: int = 3,
    exclude_ids: Sequence[str] | None = None,
) -> List[str]:
    if number_of_questions <= 0:
        return []

    exclude = set(exclude_ids or [])

    def _norm(s: str) -> str:
        return s.strip().rstrip("?").casefold()

    current_norm = _norm(current_question)

    pool = [
        question["text"]
        for question in QUESTIONS
        if question["id"] not in exclude and _norm(question["text"]) != current_norm
    ]

    if not pool:
        return []

    return random.sample(pool, k=min(number_of_questions, len(pool)))


__all__ = ["select_follow_up_questions"]
