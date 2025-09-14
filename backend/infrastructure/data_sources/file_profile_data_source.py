from pathlib import Path

class FileProfileSource:
    """Kapselt reines File-IO für das Profil-Markdown."""
    def __init__(self, md_path: Path):
        self.md_path = md_path

    def read(self) -> str:
        if not self.md_path.exists():
            raise FileNotFoundError(f"Profile file not found: {self.md_path}")
        return self.md_path.read_text(encoding="utf-8")
