import os
import cloudinary.uploader
from app.utils.cloudinary_config import cloudinary
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
    async def save_uploaded_file(file: UploadFile, user_id: str) -> dict:
        try:
            # read content
            content = await file.read()

            file_ext = file.filename.split('.')[-1].lower()
            base_name = file.filename.split('.')[0][:20].replace(" ", "_")

            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            random_str = secrets.token_hex(2)

            unique_filename = f"{base_name}_{timestamp}_{random_str}"

            upload_result = cloudinary.uploader.upload(
                content,
                public_id=f"placement_buddy/{user_id}/{unique_filename}",
                resource_type="raw"  # required for PDF, DOCX, TXT
            )

            cloudinary_url = upload_result["secure_url"]
            file_size = len(content)

            return {
                "file_url": cloudinary_url,
                "file_size": file_size,
                "original_filename": file.filename,
                "file_type": file_ext
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Cloud upload failed: {str(e)}"
            )
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
        
