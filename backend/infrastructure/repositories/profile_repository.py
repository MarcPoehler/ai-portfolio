from pathlib import Path
import json
from ...domain.ports.profile_repository import ProfileRepository as ProfileRepositoryPort
from ..data_sources.file_profile_data_source import FileProfileSource


class FileProfileRepository(ProfileRepositoryPort):
    """Composite repository reading narrative background markdown and structured profile facts (JSON).

    Returns a single synthesized markdown blob used as LLM context.
    """

    def __init__(self, path: str | Path, profile_json_path: str | Path | None = None):
        self.background_source = FileProfileSource(Path(path))
        self.profile_json_path = Path(profile_json_path) if profile_json_path else None

    def _read_background(self) -> str:
        try:
            return self.background_source.read()
        except FileNotFoundError:
            return ""

    def _read_facts(self) -> dict:
        if not self.profile_json_path or not self.profile_json_path.exists():
            return {}
        try:
            raw = self.profile_json_path.read_text(encoding="utf-8")
            return json.loads(raw)
        except Exception:
            return {"_error": "Could not parse profile.json"}

    def _build_snapshot(self, facts: dict) -> str:
        if not facts:
            return ""

        person = facts.get("person", {})
        name = person.get("name", "")
        location = person.get("location", "")
        short_bio = person.get("short_bio", "")

        highlights = facts.get("highlights", [])
        highlights_md = "\n".join(f"- {h}" for h in highlights[:8]) if highlights else "- (no highlights provided)"

        tech = facts.get("skills", {}).get("technical", [])
        technical_focus_line = ", ".join(tech[:12])

        languages = facts.get("languages", {})
        languages_line = ", ".join(f"{k} ({v})" for k, v in languages.items())

        interests = facts.get("interests", [])
        interests_line = ", ".join(interests[:10])

        snapshot = [
            "### Candidate Snapshot",
            f"**Name:** {name}  |  **Location:** {location}",
            f"**Bio:** {short_bio}" if short_bio else "",
            "**Highlights:**",
            highlights_md,
            f"**Technical Focus:** {technical_focus_line}" if technical_focus_line else "",
            f"**Languages:** {languages_line}" if languages_line else "",
            f"**Interests:** {interests_line}" if interests_line else "",
            "",
            "---",
            "",
        ]
        return "\n".join([s for s in snapshot if s is not None])


    # Public API (Port)
    def get_profile_text(self) -> str:
        background_md = self._read_background()
        facts = self._read_facts()
        snapshot = self._build_snapshot(facts)
        combined = snapshot + background_md
        return combined
