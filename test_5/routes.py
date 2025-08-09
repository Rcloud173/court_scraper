from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlite3 import connect, Row
from pathlib import Path
from app.config import DB_PATH
from app.scraper import fetch_latest_judgments
from app.models import init_db
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent/"static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent/"templates")

@app.on_event("startup")
def initialize():
    with connect(DB_PATH) as conn:
        conn.row_factory = Row
        init_db(conn)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/fetch")
async def fetch_judgments(request: Request):
    try:
        judgments = fetch_latest_judgments()
        
        with connect(DB_PATH) as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            
            for judgment in judgments:
                cursor.execute("""
                INSERT OR IGNORE INTO judgments 
                (case_no, judgment_date, petitioner, respondent, pdf_url, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    judgment['case_no'],
                    judgment['judgment_date'],
                    judgment['petitioner'],
                    judgment['respondent'],
                    judgment['pdf_url'],
                    judgment['timestamp']
                ))
            
            conn.commit()
        
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "judgments": judgments,
                "count": len(judgments)
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=500
        )

@app.get("/download")
async def download_pdf(url: str):
    if not url or not url.startswith(BASE_URL):
        raise HTTPException(status_code=400, detail="Invalid PDF URL")
    return RedirectResponse(url)