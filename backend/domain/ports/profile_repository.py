from typing import Protocol

class ProfileRepository(Protocol):
    """Outbound port: domain needs profile text but not its source.
    Implementations (file, DB, RAG, etc.) live in infrastructure layer.
    """
    def get_profile_text(self) -> str:
        ...
