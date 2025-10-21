from app.ml.preprocessor import TextPreprocessor
from app.ml.skill_extractor import SkillExtractor
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.preprocessor=TextPreprocessor()
        self.skill_extractor=SkillExtractor()
    
    def analyze_resume(self,resume_text:str,filepath:str)->Dict:
        try:
            logger.info("Starting resume analysis")
            sections=self.preprocessor.extract_sections(resume_text)
            logger.info(f"Extracted {len(sections)} sections")

            contact_info=self.preprocessor.extract_contact_info(resume_text,filepath)
            logger.info(f"Contact info: {contact_info}")

            skills_data=self.skill_extractor.extract_skills(resume_text)
            if sections.get('skills'):
                section_skills=self.skill_extractor.extract_skills_from_section(
                    sections['skills']
                )
                all_skills = set(skills_data['all_skills'] + section_skills)
                skills_data['all_skills'] = sorted(list(all_skills))

                tech_skills=[s for s in all_skills if s in self.skill_extractor.technical_skills]
                soft_skills = [s for s in all_skills if s in self.skill_extractor.soft_skills]

                skills_data['technical_skills'] = sorted(tech_skills)
                skills_data['soft_skills'] = sorted(soft_skills)

            logger.info(f"Found {len(skills_data['all_skills'])} skills")
            skill_categories = self.skill_extractor.categorize_skills(
                skills_data['technical_skills']
            )

            years_of_experience= self.preprocessor.extract_years_of_experience(sections.get('experience', ''))

            entities = self.preprocessor.extract_entities(resume_text)


            analysis_result = {
                'contact_info': contact_info,
                'sections': sections,
                'skills': skills_data,
                'skill_categories': skill_categories,
                'years_of_experience': years_of_experience,
                'entities': entities, 
                'resume_length': len(resume_text),
                'word_count': len(resume_text.split())
            }

            logger.info("Resume analysis completed successfully")
            return analysis_result
        except Exception as e:
            logger.error(f"Error inside MLService.analyze_resume: {e}")
            return {
                'contact_info': {},
                'sections': {},
                'skills': {'all_skills': [], 'technical_skills': [], 'soft_skills': []}, # Minimal structure required by caller
                'skill_categories': {},
                'years_of_experience': 0,
                'entities': [], 
                'resume_length': 0,
                'word_count': 0
            } 
    
    def extract_key_highlights(self, analysis: Dict) -> List[str]:
        highlights = []
        if analysis.get('years_of_experience', 0) > 0:
            highlights.append(f"{analysis['years_of_experience']} years of experience")
        
        tech_skills_count = len(analysis['skills']['technical_skills'])
        if tech_skills_count > 0:
            highlights.append(f"{tech_skills_count} technical skills identified")
        
        skill_cats = analysis.get('skill_categories', {})
        if skill_cats:
            top_category = max(skill_cats.items(), key=lambda x: len(x[1]))
            highlights.append(f"Strong in {top_category[0].replace('_', ' ').title()}")
    
        companies = analysis['entities'].get('organizations', [])
        if companies:
            highlights.append(f"Experience at: {', '.join(companies[:3])}")
        
        return highlights