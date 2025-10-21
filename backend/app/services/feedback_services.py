from openai import OpenAI
from app.config import settings
from app.ml.prompts import ResumePrompts
import json
import logging
import re

logger=logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class FeedbackService:
    @staticmethod
    def safe_feedback(ai_feedback):
        fallback = FeedbackService._get_fallback_feedback()
        if not ai_feedback or not isinstance(ai_feedback, dict):
            ai_feedback = fallback
        # Ensure all keys exist and are not None
        ai_feedback['overall_score'] = ai_feedback.get('overall_score') or fallback['overall_score']
        ai_feedback['feedback_sections'] = ai_feedback.get('feedback_sections') or fallback['feedback_sections']
        ai_feedback['top_suggestions'] = ai_feedback.get('top_suggestions') or fallback['top_suggestions']
        ai_feedback['top_strengths'] = ai_feedback.get('top_strengths') or fallback.get('top_strengths', [])
        return ai_feedback

    async def generate_resume_feedback(self,resume_text: str, extracted_skills: list)->dict:
        try:
            logger.info("Generating feedback with OpenAI GPT-4...")
            prompt=ResumePrompts.get_resume_analysis_prompt(resume_text, extracted_skills)
            response= client.chat.completions.create(
                model="gpt-4o",  # or "gpt-3.5-turbo"
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume reviewer and career coach with 15+ years of experience in recruiting and talent acquisition."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            raw_text = response.choices[0].message.content.strip()
            logger.debug(raw_text)
            match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL | re.IGNORECASE)
            if match:
                raw_text = match.group(1)
            try:
                feedback = json.loads(raw_text)
            except json.JSONDecodeError:
                logger.warning("OpenAI returned non-JSON output. Using fallback.")
                feedback = FeedbackService._get_fallback_feedback()

            return feedback
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return FeedbackService._get_fallback_feedback()
        
    @staticmethod
    def _get_fallback_feedback() -> dict:
        return {
            "overall_score": 70,
            "feedback_sections": [
                {
                    "category": "Content Quality",
                    "score": 70,
                    "strengths": ["Resume contains relevant information"],
                    "suggestions": ["Add more quantifiable achievements", "Use stronger action verbs"]
                },
                {
                    "category": "Format & Structure",
                    "score": 65,
                    "strengths": ["Basic structure is present"],
                    "suggestions": ["Improve section organization", "Ensure consistent formatting"]
                }
            ],
            "top_strengths":[
                "Clear and concise language",
                "Relevant experience highlighted"
            ],
            "top_suggestions": [
                "Add metrics and numbers to demonstrate impact",
                "Improve keyword usage for ATS optimization",
                "Highlight achievements over responsibilities"
            ]
        }
    

    @staticmethod
    def calculate_ats_score(resume_text: str, skills: list) -> dict:
        score = 100
        issues = []
        recommendations = []
        
        # Length (1-2 pages is ideal)
        word_count = len(resume_text.split())
        if word_count < 300:
            score -= 15
            issues.append("Resume is too short")
            recommendations.append("Expand your experience and achievements")
        elif word_count > 1000:
            score -= 10
            issues.append("Resume is too long")
            recommendations.append("Condense to 1-2 pages")
        
        if 'skills' in resume_text.lower() or 'technical skills' in resume_text.lower():
            pass
        else:
            score -= 20
            issues.append("No dedicated skills section found")
            recommendations.append("Add a clear 'Skills' section")
        
        # Check 3: Contact information
        
        has_email = bool(re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', resume_text))
        has_phone = bool(re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', resume_text))
        
        if not has_email:
            score -= 15
            issues.append("Email not found")
            recommendations.append("Add your email address")
        
        if not has_phone:
            score -= 10
            issues.append("Phone number not found")
            recommendations.append("Add your phone number")
        
        # Check 4: Number of skills
        if len(skills) < 5:
            score -= 15
            issues.append("Limited technical skills listed")
            recommendations.append("Add more relevant technical skills")
        
        # Check 5: Common ATS-friendly sections
        required_sections = ['experience', 'education']
        for section in required_sections:
            if section not in resume_text.lower():
                score -= 10
                issues.append(f"'{section.title()}' section not clearly identified")
                recommendations.append(f"Add a clear '{section.title()}' section")
        
        return {
            "ats_score": max(0, score),
            "issues": issues,
            "recommendations": recommendations,
            "is_ats_friendly": score >= 70
        }