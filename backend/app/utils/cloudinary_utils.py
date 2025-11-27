import cloudinary.uploader
import re

def delete_from_cloudinary(file_url: str) -> bool:
    """
    Extracts Cloudinary public_id from URL and deletes the file.
    Works for raw uploads like PDFs, DOCX, etc.
    """
    try:
        match = re.search(r"/upload/(?:v\d+/)?(.+)$", file_url)
        if not match:
            return False
        
        public_id = match.group(1)

        # Delete RAW file
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type="raw"
        )
        return result.get("result") in ["ok", "not found"]

    except Exception as e:
        print("Cloudinary deletion error:", e)
        return False
