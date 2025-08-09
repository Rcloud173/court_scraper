import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from config import DB_PATH

BASE_URL = "https://delhihighcourt.nic.in"
JUDGMENTS_URL = f"{BASE_URL}/web/judgement/fetch-data"

def fetch_latest_judgments():
    """Fetch and parse latest judgments from Delhi HC website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(JUDGMENTS_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        judgments = []
        
        # Extract table rows (skip header row)
        rows = soup.select('table tr')[1:]
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:  # Ensure all columns exist
                continue
                
            case_no = cols[1].get_text(strip=True)
            judgment_date = cols[2].get_text(strip=True)
            petitioner = cols[3].get_text(strip=True)
            respondent = cols[4].get_text(strip=True)
            
            # Extract PDF link
            pdf_link = cols[5].find('a', href=True)
            pdf_url = urljoin(BASE_URL, pdf_link['href']) if pdf_link else None
            
            judgments.append({
                'case_no': case_no,
                'judgment_date': judgment_date,
                'petitioner': petitioner,
                'respondent': respondent,
                'pdf_url': pdf_url,
                'timestamp': datetime.now().isoformat()
            })
        
        return judgments
        
    except Exception as e:
        print(f"Error fetching judgments: {str(e)}")
        return []