from app.models.resume import Resume
from typing import Dict, Optional, List
from datetime import datetime

class ResumeService:
    @staticmethod
    async def create_resume_record(
        user_id:str,
        filename:str,
        filepath:str,
    )->Resume:
        new_resume= Resume(
            user_id=user_id,
            filename=filename,
            filepath=filepath,
            uploaded_at=datetime.utcnow()
        )

        await new_resume.insert()
        return new_resume
        
    @staticmethod
    async def delete_resume_record(file_path: str, user_id: str)->bool:
        result = await Resume.find_one(
            Resume.filepath == file_path,
            Resume.user_id == user_id
        ).delete()

        return result.deleted_count > 0
    
    @staticmethod
    async def update_raw_text(
        file_path: str,
        user_id: str,
        cleaned_text: str
    )->Optional[Resume]:
        resume = await Resume.find_one(
            Resume.filepath == file_path,
            Resume.user_id == user_id
        )
        if not resume:
            return None
        
        resume.raw_text = cleaned_text
        await resume.save()
        return resume