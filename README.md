# Court Data Fetcher & web app

## 📌 Overview
This is a FastAPI-based web application that fetches and displays **latest judgments** from the Delhi High Court public website.  
The app allows users to search cases by case type, number, and filing year, fetches metadata, and provides direct links to download judgment/order PDFs.

**Key Features:**
- HTML form for entering case details.
- Web scraper to retrieve latest court judgments.
- SQLite database for query logging and judgment storage.
- Clean results page with downloadable PDF links.
- Error handling for invalid cases and downtime.

---

## 🎯 Functional Requirements Implementation

| Requirement | Status |
|-------------|--------|
| UI form with Case Type, Case Number, Filing Year | ✅ Implemented (`index.html`) |
| Backend scraping (bypass view-state tokens/CAPTCHA if needed) | ✅ Implemented for Delhi HC |
| Parse parties’ names, filing & hearing dates, latest PDF links | ✅ Implemented |
| Storage in SQLite/PostgreSQL | ✅ SQLite implemented |
| Display parsed data + PDF download option | ✅ Implemented |
| User-friendly error messages | ✅ Implemented |

---

## 🛠 Technology Stack
- **Backend:** FastAPI (Python 3.10+)
- **Frontend:** HTML + Jinja2 Templates
- **Database:** SQLite (via `sqlite3` module)
- **Scraping:** `requests`, `BeautifulSoup4`
- **Server:** Uvicorn

---

## 📂 Project Structure
project_root/
│
├── config.py # Paths and directory setup
├── main.py # FastAPI app entry point
├── models.py # Database schema definitions
├── routes.py # Alternate routing file (optional)
├── scraper.py # Judgment scraping logic
├── templates/ # HTML templates (index, results, error)
├── static/ # Static assets (CSS, JS)
├── database/ # SQLite database location
└── check_db.py # Utility to count DB records


---

## ⚙️ Setup Instructions

---

### 1. Clone Repository
bash
git clone https://github.com/yourusername/court-data-fetcher.git
cd court-data-fetcher

---

### 2. Install Dependencies

pip install fastapi uvicorn requests beautifulsoup4

---

### 3. Run Application

uvicorn main:app --reload

---

## 🔍 Usage

1. Open the home page (`/`) to see the **case search form**.
2. Fill in:
   - **Case Type** (e.g., WP, CRL)
   - **Case Number**
   - **Filing Year**
3. Click **Search** → The app will scrape the Delhi HC site for the latest judgments.
4. The results page will display:
   - Case number
   - Judgment date
   - Petitioner & Respondent
   - PDF download link
5. Click **Download** to open the PDF directly.

---

## 🗄 Database Schema

### `judgments` Table
| Column         | Type     | Notes |
|----------------|----------|-------|
| id             | INTEGER  | Primary key, autoincrement |
| case_no        | TEXT     | Case number |
| judgment_date  | TEXT     | Date as string |
| petitioner     | TEXT     | Petitioner name |
| respondent     | TEXT     | Respondent name |
| pdf_url        | TEXT     | Direct PDF URL |
| timestamp      | TEXT     | ISO 8601 fetch time |

### `queries` Table *(Optional)*
| Column         | Type     | Notes |
|----------------|----------|-------|
| id             | INTEGER  | Primary key, autoincrement |
| case_type      | TEXT     | Case type |
| case_number    | TEXT     | Case number |
| filing_year    | TEXT     | Year filed |
| timestamp      | DATETIME | Default current time |

---

## 📜 Scraper Details

- **Source:** [Delhi High Court](https://delhihighcourt.nic.in)
- **Base URL:** `https://delhihighcourt.nic.in`
- **Data Endpoint:** `/web/judgement/fetch-data`
- **Method:** `GET`
- **Parser:** BeautifulSoup (HTML `<table>` parsing)

**Captured Fields:**
- Case Number
- Judgment Date
- Petitioner
- Respondent
- PDF URL

---

## 🚦 Error Handling
- **Network failure** → Shows `error.html` with status 500.
- **Invalid PDF URL** → Returns HTTP 400.
- **Duplicate entries** → Skipped via `INSERT OR IGNORE`.
- **Missing data rows** → Skipped in scraper.

---

## 📌 Known Issues & Future Improvements
- **CAPTCHA Handling:** Not implemented — scraper will fail if CAPTCHA is enforced.
- **District Court Support:** Currently hardcoded for Delhi High Court; scraper logic must be adapted for other courts.
- **`routes.py` Bug:** Missing `BASE_URL` import in `/download`.
- **`queries` Table:** Defined but unused in main workflow.

---

## 👤 Author
- **Name:** Amir Shaikh 
- **Role:** Robotics + AI Enthusiast  
- **Internship:** Court Data Fetcher & Mini-Dashboard
