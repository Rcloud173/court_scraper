import requests
import datetime
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import DB_PATH

BASE = "https://delhihighcourt.nic.in"
JUDGMENTS_URL = f"{BASE}/web/judgement/fetch-data"

def run():
    """Scrape Delhi High Court judgments and store in DB."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Ensure table exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS judgments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetched_at TEXT,
        case_number TEXT,
        judgment_date TEXT,
        petitioner TEXT,
        respondent TEXT,
        pdf_url TEXT,
        raw_html BLOB
    )
    """)
    cur.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_case_date 
    ON judgments(case_number, judgment_date)
    """)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JudgmentFetcher/1.0)"
    }
    r = requests.get(JUDGMENTS_URL, headers=headers, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tr")
    if len(rows) <= 1:
        raise ValueError("No rows found – HTML structure may have changed.")

    data_rows = rows[1:]
    inserted = 0

    for tr in data_rows:
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue

        case_no = tds[0].get_text(strip=True)
        j_date = tds[1].get_text(strip=True)
        petitioner = tds[2].get_text(strip=True)
        respondent = tds[3].get_text(strip=True)

        pdf_url = None
        a = tr.find("a", href=True)
        if a:
            pdf_url = urljoin(BASE, a["href"])

        cur.execute(
            "SELECT 1 FROM judgments WHERE case_number = ? AND judgment_date = ?",
            (case_no, j_date)
        )
        if cur.fetchone():
            continue

        raw_html = str(tr).encode("utf-8")
        cur.execute("""
            INSERT INTO judgments
            (fetched_at, case_number, judgment_date, petitioner, respondent, pdf_url, raw_html)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now(datetime.UTC).isoformat(),
            case_no,
            j_date,
            petitioner,
            respondent,
            pdf_url,
            raw_html
        ))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted

if __name__ == "__main__":
    print("Fetched", run(), "new judgments")


