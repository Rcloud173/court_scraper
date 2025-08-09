from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "database" / "judgments.db"

# Ensure directories exist
os.makedirs(BASE_DIR / "database", exist_ok=True)
os.makedirs(BASE_DIR / "static", exist_ok=True)
os.makedirs(BASE_DIR / "templates", exist_ok=True)