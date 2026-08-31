import json
from pathlib import Path


class LottieAnimationLoader:
    """Optional Lottie metadata loader; the built-in renderer works without JSON assets."""

    def __init__(self, directory: Path):
        self.directory = directory

    def load(self, name: str) -> dict | None:
        path = self.directory / f"{name}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
