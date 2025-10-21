import pdfplumber
from docx import Document
from fastapi import HTTPException
import re
class PDFParserService:
    @staticmethod
    def extract_text_from_pdf(file_path:str)->str:
        text=""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()# Remove trailing newline    
        except Exception as e:
            print(f"Error extracting text from PDF using pdfPlumber: {e}") 


    @staticmethod
    def extract_text_from_docx(file_path:str)->str:
        text=""
        try:
            doc= Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + "\t"
                    text += "\n"

            if not text.strip():
                raise HTTPException(status_code=500, detail="DOCX file appears to be empty or unreadable")
            return text  
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract text from DOCX: {str(e)}"
            )


    @staticmethod
    def parse_resume(file_path:str,file_type:str)->str:
        print(file_type)
        if file_type == "pdf":
            return PDFParserService.extract_text_from_pdf(file_path)
        elif file_type == "docx":
            return PDFParserService.extract_text_from_docx(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type for parsing")
    
    @staticmethod
    def clean_text(text:str)->str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        text=text.strip()
        return text