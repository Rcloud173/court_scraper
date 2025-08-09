from sqlite3 import Connection
from app.config import DB_PATH

def init_db(conn: Connection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_type TEXT,
        case_number TEXT,
        filing_year TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS judgments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_no TEXT,
        judgment_date TEXT,
        petitioner TEXT,
        respondent TEXT,
        pdf_url TEXT,
        timestamp TEXT,
        UNIQUE(case_no, judgment_date)
    )
    """)