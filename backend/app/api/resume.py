from fastapi import APIRouter, File, UploadFile, HTTPException,Depends
import os
from bson import ObjectId
from app.schemas.jd_match import JDMatchRequest
from app.utils.cloudinary_utils import delete_from_cloudinary
from app.services.file_services import FileService
from app.services.resume_services import ResumeService
from app.services.parser_services import PDFParserService
from app.services.jd_match_service import JDMatchService
from app.services.ml_services import MLService
from app.services.feedback_services import FeedbackService
from app.models.resume import Resume
from app.models.analysis import Analysis
from bson import ObjectId
from datetime import datetime
from app.utils.security import get_current_user
import logging
router=APIRouter()
logger = logging.getLogger(__name__)

@router.post("/match")
async def match_resume_with_jd(
    data: JDMatchRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Matches stored resume analysis against a pasted job description.
    """

    # Fetch analysis
    analysis = await Analysis.find_one(
        Analysis.id == ObjectId(data.analysis_id),
        Analysis.user_id == user_id
    )
    if not analysis:
        raise HTTPException(404, "Resume analysis not found")

    # Fetch resume using analysis.resume_id
    resume = await Resume.find_one(
        Resume.id == ObjectId(analysis.resume_id),
        Resume.user_id == user_id
    )
    if not resume:
        raise HTTPException(404, "Linked resume not found")

    # Extract data
    resume_text = resume.raw_text
    analysis_results = analysis.dict()

    # Pass to AI matching service
    match_result = await JDMatchService.match(
        resume_text=resume_text,
        analysis_results=analysis_results,
        job_description=data.job_description
    )

    return {
        "success": True,
        "analysis_id": data.analysis_id,
        "match_result": match_result
    }
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    FileService.validate_file(file)
    file_info = await FileService.save_uploaded_file(file, user_id)
    file_url = file_info["file_url"]
    file_type = file_info["file_type"]
    raw_text = PDFParserService.parse_resume(file_url, file_type)

    if not raw_text:
        raise HTTPException(
            status_code=404,
            detail="Could not extract any content from the uploaded resume."
        )

    cleaned_text = PDFParserService.clean_text(raw_text)
    try:
        resume_record = await ResumeService.create_resume_record(
            user_id=user_id,
            filename=file_info["original_filename"],
            file_url=file_url    # UPDATED
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create resume record: {str(e)}"
        )

    # Update cleaned text in DB
    updated_resume = await ResumeService.update_raw_text(
        file_url=file_url,      # UPDATED
        user_id=user_id,
        cleaned_text=cleaned_text
    )

    if not updated_resume:
        raise HTTPException(
            status_code=404,
            detail="Resume record not found after upload."
        )

    return {
        "message": "Resume uploaded and processed successfully",
        "file_url": file_url,
        "resume_id": str(resume_record.id),
        "raw_text_length": len(cleaned_text),
        "status": "UPLOAD_OK"
    }

@router.delete("/delete")
async def delete_resume(
    file_url: str,
    user_id: str = Depends(get_current_user)
):
    if user_id not in file_url.replace("/", ""):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own uploaded files."
        )
    cloud_deleted = delete_from_cloudinary(file_url)
    db_deleted = await ResumeService.delete_resume_record(file_url, user_id)
    if cloud_deleted and db_deleted:
        return {"message": "Resume deleted from Cloudinary and database successfully"}

    if db_deleted and not cloud_deleted:
        return {"message": "Database record deleted, but file not found on Cloudinary"}

    if cloud_deleted and not db_deleted:
        return {"message": "Cloudinary file deleted, but database record not found"}

    raise HTTPException(
        status_code=404,
        detail="Resume not found on Cloudinary or in database"
    )
@router.post("/analyze/{resume_id}")
async def analyze_resume(resume_id:str):
    try:
        resume=await Resume.find_one({"_id": ObjectId(resume_id)})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_text=resume.raw_text
        await resume.save()
        logger.info(f"Starting analysis for resume ID: {resume_id}")
        ml_service=MLService()
        analysis=ml_service.analyze_resume(resume_text,resume.file_url)
        feedback_service=FeedbackService()
        try:
            ai_feedback = await feedback_service.generate_resume_feedback(
                resume_text, analysis['skills']['all_skills']
            )
        except Exception as e:
            logger.error(f"Error generating AI feedback: {e}")
            ai_feedback = FeedbackService._get_fallback_feedback()

        # Sanitize it
        print("DEBUG 1: got AI feedback")
        ai_feedback = FeedbackService.safe_feedback(ai_feedback)
        print("DEBUG 2: safe feedback done")
        ats_analysis=feedback_service.calculate_ats_score(resume_text, analysis['skills']['all_skills'])
        print("DEBUG 3: ATS analysis done")
        try:
            highlights = ml_service.extract_key_highlights(analysis)
        except Exception as e:
            logger.warning(f"Error extracting highlights: {e}")
            highlights = []
        print("DEBUG 4: highlights extracted")

        analysis_doc = {
            "resume_id": resume_id,
            "user_id": resume.user_id,
            "overall_score": ai_feedback.get('overall_score', 70),
            "ats_score": ats_analysis['ats_score'],
            "feedback_sections": ai_feedback.get('feedback_sections', []),
            "top_suggestions": ai_feedback.get('top_suggestions', []),
            "top_strength": ai_feedback.get('top_strengths', []),
            "extracted_skills": (analysis.get('skills') or {}).get('all_skills', []),
            "technical_skills": (analysis.get('skills') or {}).get('technical_skills', []),
            "soft_skills": (analysis.get('skills') or {}).get('soft_skills', []),
            "skill_categories": analysis.get('skill_categories', {}),
            "years_of_experience": analysis.get('years_of_experience', 0),
            "contact_info": analysis.get('contact_info', {}),
            "entities": analysis.get('entities') or [],
            "highlights": highlights or [],
            "ats_analysis": ats_analysis,
            "created_at": datetime.utcnow()
        }
        print(analysis_doc)
        analysis_instance = Analysis(**analysis_doc)
        result = await analysis_instance.insert()
        analysis_id = str(analysis_instance.id)
        resume.analysis_status="COMPLETED"
        resume.parsed_sections = analysis.get('sections') or {}
        resume.analysis_id=analysis_id
        await resume.save()
        logger.info(f"Analysis completed for resume: {resume_id}")
        
        return {
            "success": True,
            "message": "Analysis completed",
            "analysis_id": analysis_id,
            "results": {
                "overall_score": analysis_doc['overall_score'],
                "ats_score": analysis_doc['ats_score'],
                "skills_found": len(analysis_doc['extracted_skills']),
                "technical_skills": len(analysis_doc['technical_skills']),
                "soft_skills": len(analysis_doc['soft_skills']),
                "experience_years": analysis_doc['years_of_experience'],
                "highlights": highlights or [],
                "skill_categories": analysis_doc['skill_categories'],
                "feedback_sections": analysis_doc['feedback_sections'],
                "top_suggestions": analysis_doc['top_suggestions'],
                "ats_analysis": analysis_doc['ats_analysis'],
                "top_strength": analysis_doc['top_strength']
            },
            
        }

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        if resume:
            resume.analysis_status="FAILED"
            await resume.save()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    


  
