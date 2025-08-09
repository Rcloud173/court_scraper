import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import BASE_DIR, DB_PATH
from scraper import run as scrape_latest
from models import Judgment

app = FastAPI(title="Delhi HC Judgments")

# Mount static and templates directories from BASE_DIR in config.py
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_db():
    """Create a SQLite connection using the DB path from config.py."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Render home page with search form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch")
def fetch():
    """Trigger scraper to fetch latest judgments."""
    try:
        inserted = scrape_latest()
        return {"status": "ok", "inserted": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def log_query(case_type: Optional[str], case_number: Optional[str], filing_year: Optional[str]):
    """Log user search queries in DB."""
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                timestamp TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute(
            "INSERT INTO queries (case_type, case_number, filing_year) VALUES (?, ?, ?)",
            (case_type, case_number, filing_year)
        )
        conn.commit()
    finally:
        conn.close()

@app.post("/search", response_model=List[Judgment])
def search(caseType: Optional[str] = Form(None),
           caseNumber: Optional[str] = Form(""),
           filingYear: Optional[str] = Form("")):
    """Search judgments by case number and/or filing year."""
    log_query(caseType, caseNumber, filingYear)

    conn = get_db()
    try:
        sql = "SELECT id, case_number, judgment_date, petitioner, respondent, pdf_url FROM judgments WHERE 1=1"
        params = []
        if caseNumber:
            sql += " AND case_number LIKE ?"
            params.append(f"%{caseNumber.strip()}%")
        if filingYear:
            sql += " AND judgment_date LIKE ?"
            params.append(f"%{filingYear.strip()}%")
        sql += " ORDER BY id DESC LIMIT 200"
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@app.get("/judgments", response_model=List[Judgment])
def list_judgments(q: str = ""):
    """List stored judgments, optionally filtering by search term."""
    conn = get_db()
    try:
        sql = "SELECT id, case_number, judgment_date, petitioner, respondent, pdf_url FROM judgments WHERE 1=1"
        params = []
        if q:
            sql += " AND (case_number LIKE ? OR petitioner LIKE ? OR respondent LIKE ?)"
            params.extend([f"%{q}%"] * 3)
        sql += " ORDER BY id DESC LIMIT 500"
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@app.get("/download/{jid}")
def download(jid: int):
    """Redirect to stored PDF URL for a judgment."""
    conn = get_db()
    try:
        row = conn.execute("SELECT pdf_url FROM judgments WHERE id=?", (jid,)).fetchone()
    finally:
        conn.close()

    if not row or not row["pdf_url"]:
        raise HTTPException(status_code=404, detail="PDF not found")

    pdf_url = row["pdf_url"]
    if pdf_url.startswith(("http://", "https://")):
        return RedirectResponse(pdf_url)
    return JSONResponse({"url": pdf_url})


