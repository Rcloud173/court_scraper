# Create a temporary check_db.py file in your test_5 directory
import sqlite3
from config import DB_PATH

def count_judgments():
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM judgments")
        count = cursor.fetchone()[0]
        print(f"Found {count} judgments in database")
        
if __name__ == "__main__":
    count_judgments()