from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models" / "vosk-model-small-en-us-0.15"

APP_TITLE = "Hamster Lock Screen"
UNLOCK_PHRASE = "open sesame"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
IDLE_SLEEP_SECONDS = 30.0
MAX_ATTEMPTS = 5

COLORS = {
    "ink": (8, 12, 28),
    "panel": (18, 24, 48),
    "panel_light": (29, 38, 70),
    "cream": (255, 245, 216),
    "muted": (159, 173, 207),
    "cyan": (83, 225, 223),
    "pink": (244, 113, 146),
    "red": (239, 92, 109),
    "green": (112, 225, 158),
    "gold": (255, 202, 92),
}
