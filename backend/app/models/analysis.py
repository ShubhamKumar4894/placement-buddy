from beanie import Document
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from pydantic import Field
class Analysis(Document):
    
    resume_id: str
    user_id: str
    overall_score: Optional[float] = 70
    ats_score: Optional[float] = 0
    feedback_sections: Optional[List[Dict[str, Any]]] = []
    top_suggestions: Optional[List[str]] = []
    top_strength: Optional[List[str]] = []
    extracted_skills: Optional[List[str]] = []
    technical_skills: Optional[List[str]] = []
    soft_skills: Optional[List[str]] = []
    skill_categories: Optional[Dict[str, List[str]]] = {}
    years_of_experience: Optional[float] = 0
    contact_info: Optional[Dict[str, str]] = {}
    entities: Optional[List[Dict[str, Any]]] = []
    highlights: Optional[List[str]] = []
    ats_analysis: Optional[Dict[str, Any]] = {}
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "analyses"
