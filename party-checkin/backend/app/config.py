from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "attendees.db"

EVENT_NAME = "Mid Year Team Get Together"

CHECKIN_START = "18:30"

CHECKIN_END = "22:00"