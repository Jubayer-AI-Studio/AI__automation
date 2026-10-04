import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
MUSIC_DIR = ASSETS_DIR / "music"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font path with Nirmala fallback on Windows
FONT_PATH = FONTS_DIR / "HindSiliguri-Bold.ttf"
if not FONT_PATH.exists() and os.path.exists("C:/Windows/Fonts/Nirmala.ttc"):
    FONT_PATH = Path("C:/Windows/Fonts/Nirmala.ttc")

BGM_PATH = MUSIC_DIR / "mystery_bgm.mp3"

# Load .env file with utf-8-sig to automatically strip any Windows BOM
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                val = v.strip()
                key = k.strip()
                if val:
                    os.environ[key] = val

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip() or "8638569113:AAHwY2Rd9Ueyx9kWKAGv6VYDELKnfRdQtEc"
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip() or "8273323826"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip() or "AQ.Ab8RN6JDCgqPoakWFdH2q0aaN2eykJm8rTrplZQ1DyJV25z5cg"
GROK_API_KEY = os.getenv("GROK_API_KEY", "").strip() or os.getenv("XAI_API_KEY", "").strip()

# Video specs
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30
VOICE_NAME = "bn-BD-PradeepNeural"

