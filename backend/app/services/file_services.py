import os
import aiofiles 
from fastapi import UploadFile,HTTPException
from app.config import settings
from datetime import datetime
import secrets
from pathlib import Path

class FileService:
    @staticmethod
    def validate_file(file: UploadFile) -> bool:
        allowed_extensions = {"pdf", "docx"}
        
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type .{file_ext} not allowed. Allowed: {allowed_extensions}"
            )
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        return True
    
    @staticmethod
    async def save_uploaded_file(file:UploadFile,user_id:str)->dict:
        cleaned_user_id = user_id.strip(' /\\')
        
        file_ext = file.filename.split('.')[-1].lower()
        base_name = os.path.splitext(file.filename)[0][:20]
        base_name = base_name.replace(" ", "_")

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        random_str = secrets.token_hex(2)

        unique_filename = f"{base_name}_{timestamp}_{random_str}.{file_ext}"

        base_upload_path = Path(settings.UPLOAD_DIR) / "uploads"
        base_upload_path = base_upload_path.resolve() 

        user_upload_path = base_upload_path / cleaned_user_id
        
        user_upload_path.mkdir(parents=True, exist_ok=True)
        file_path = str(user_upload_path / unique_filename)
        
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            file_size=len(content)    
               
            if(file_size > 5 * 1024 * 1024):  # 5MB limit
                os.remove(file_path)
                raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")
            return {
                "file_path": file_path,
                "file_size": file_size,
                "original_filename": file.filename,
                "file_type": file_ext
            }
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")    
        
    @staticmethod
    def delete_file(file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
            return False
        
