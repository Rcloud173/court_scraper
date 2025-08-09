# models.py
from pydantic import BaseModel
from typing import Optional

class Judgment(BaseModel):
    id: int
    case_number: str
    judgment_date: str
    petitioner: Optional[str] = ""
    respondent: Optional[str] = ""
    pdf_url: Optional[str] = None
