"""Catalog of predefined follow-up questions.

Each entry has:
- id: stable identifier (snake_case)
- text: the question shown to the user

"""

from __future__ import annotations

from typing import List, Dict

QuestionEntry = Dict[str, object]

QUESTIONS: List[QuestionEntry] = [
    {"id": "impact_project", "text": "What project are you most proud of?"},
    {"id": "ai_content_production", "text": "How did you enable AI-assisted content production at simpleclub?"},
    {"id": "reliability_llm", "text": "How do you ensure reliability of LLM outputs in production?"},
    {"id": "decision_framework", "text": "How do you decide between RAG, fine-tuning, prompt-only, and agents?"},
    {"id": "quality_llm", "text": "How do you define and measure quality in LLM outputs?"},
    {"id": "guardrails_privacy", "text": "What guardrails do you use for privacy and compliance?"},
    {"id": "monitoring_production", "text": "How do you monitor AI systems in production?"},
    {"id": "api_design", "text": "What is your approach to API design for AI features?"},
    {"id": "cross_team_adoption", "text": "How do you foster cross-team adoption of new AI workflows?"},
    {"id": "failed_rollout", "text": "What did you learn from an AI rollout that didn’t succeed?"},
    {"id": "prototype_features", "text": "Describe the free-text evaluation or media asset generation prototypes you built."},
    {"id": "business_alignment", "text": "How do you align technical design with business impact?"},
]

__all__ = ["QUESTIONS", "QuestionEntry"]
