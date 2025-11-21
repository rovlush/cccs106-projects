from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_UNITS = os.getenv("DEFAULT_UNITS", "metric")  # "metric" or "imperial"

if not OPENWEATHER_API_KEY:
    raise ValueError("Please set OPENWEATHER_API_KEY in your .env file.")

ROOT = Path(__file__).parent
HISTORY_FILE = ROOT / "search_history.json"
# Path to the screenshot you uploaded in this chat session (used as header/logo).
UPLOADED_HEADER_PATH = Path("/mnt/data/88c86e1d-fe32-4c62-94cb-99f1d2692a53.jpg")
ASSETS_DIR = ROOT / "assets"