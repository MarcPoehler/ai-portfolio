# backend/config.py
import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

def _split_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

@dataclass
class Settings:
    """Central runtime configuration."""
    # App
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Data
    data_dir: str = os.getenv("DATA_DIR", "data")
    background_file: str = os.getenv("BACKGROUND_FILE", "background.md")
    profile_json_file: str = os.getenv("PROFILE_JSON_FILE", "profile.json")

    # PII
    pii_enabled: bool = os.getenv("PII_ENABLED", "true").lower() == "true"
    pii_block_severity: str = os.getenv("PII_BLOCK_SEVERITY", "high")
    pii_mask: bool = os.getenv("PII_MASK", "true").lower() == "true"

    # OpenAI / LLM
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # Follow-up questions
    follow_up_questions_count: int = int(os.getenv("FOLLOW_UP_QUESTIONS_COUNT", "3"))

    # Delivery / CORS
    cors_allowed_origins: List[str] = field(
        default_factory=lambda: _split_csv(os.getenv("CORS_ALLOWED_ORIGINS"))
    )
