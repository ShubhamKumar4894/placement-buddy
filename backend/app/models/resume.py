from beanie import Document
from typing import Optional, Dict, List
from datetime import datetime
from datetime import timezone
from pydantic import  Field

class Resume(Document):
    user_id: str          # ObjectId as str or user.id
    filename: str
    filepath: str
    raw_text: Optional[str] = None
    parsed_sections: Optional[Dict] = None
    analysis_status: str = Field(default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    embeddings: Optional[List[float]] = None
    analysis_id: Optional[str] = None 
    uploaded_at: datetime = datetime.utcnow()

    class Settings:
        name = "resumes"
