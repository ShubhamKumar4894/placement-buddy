from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional
from datetime import timezone

class User(Document):
    email: EmailStr
    hashed_password: Optional[str] = None    # null for OAuth users
    full_name: Optional[str] = None
    oauth: Optional[dict] = None
    
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"
