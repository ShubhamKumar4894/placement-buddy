class ResumePrompts:

    @staticmethod
    def get_resume_analysis_prompt(resume_text: str, extracted_skills: list) -> str:

        SYSTEM_PROMPT= f"""
            You are an expert resume reviewer and career coach. Analyze the following resume and provide detailed, actionable feedback.

        Resume Text: {resume_text}
        
        Detected Skills: {', '.join(extracted_skills) if extracted_skills else 'None detected'}
        
        Provide your analysis in the following JSON format:
        {{
            "overall_score": 0,
            "feedback_sections": [
                {{
                    "category": "Content Quality",
                    "score": 0,
                    "strengths": [],
                    "suggestions": []
                }},
                {{
                    "category": "Format & Structure",
                    "score": 0,
                    "strengths": [],
                    "suggestions": []
                }},
                {{
                    "category": "Keywords & ATS Optimization",
                    "score": 0,
                    "strengths": [],
                    "suggestions": []
                }},
                {{
                    "category": "Impact & Achievements",
                    "score": 0,
                    "strengths": [],
                    "suggestions": []
                }}
            ],
            "top_strengths": [],  # Merge all strengths from above
            "top_suggestions": [] # Merge all suggestions from above
        }}

            Focus on:
            1. Content quality and relevance
            2. Formatting and readability
            3. ATS (Applicant Tracking System) compatibility
            4. Use of action verbs and quantifiable achievements
            5. Skills presentation
            6. Overall professional impact

        Be specific, actionable, and constructive. """
        return SYSTEM_PROMPT
    
    @staticmethod
    def get_job_match_prompt(resume_text: str, job_description: str, resume_skills: list) -> str:
        SYSTEM_PROMPT= f"""
            You are an expert recruiter analyzing a candidate's resume against a job description.
            Resume : {resume_text}

            Resume Skills: {', '.join(resume_skills) if resume_skills else 'None detected'}

            Job Description:
            {job_description}

            Analyze the match and provide your assessment in the following JSON format:
            {{
                "match_percentage": <number between 0-100>,
                "matched_skills": ["skill1", "skill2", "skill3"],
                "missing_skills": ["skill1", "skill2", "skill3"],
                "experience_match": {{
                    "required_years": <number or null>,
                    "candidate_years": <number or null>,
                    "match": <"excellent" | "good" | "fair" | "poor">
                }},
                "recommendations": [
                    "Specific recommendation 1",
                    "Specific recommendation 2",
                    "Specific recommendation 3"
                ],
                "strengths": [
                    "Key strength 1",
                    "Key strength 2"
                ],
                "gaps": [
                    "Gap 1 with severity",
                    "Gap 2 with severity"
                ]
            }}

            Calculate match_percentage based on:
            - Skills overlap (40%)
            - Experience relevance (30%)
            - Education match (15%)
            - Other requirements (15%)

        Be honest and specific about gaps while highlighting strengths."""

        return SYSTEM_PROMPT
    @staticmethod
    def get_skill_gap_analysis_prompt(resume_skills: list, job_skills: list) -> str:
        SYSTEM_PROMPT=f"""
        Analyze the skill gap between a candidate and a job requirement.
        Candidate Skills: {', '.join(resume_skills) if resume_skills else 'None'}
        Required Skills: {', '.join(job_skills) if job_skills else 'None'}

        Provide analysis in JSON format:
        {{
            "critical_missing_skills": ["skill1", "skill2"],
            "nice_to_have_missing_skills": ["skill1", "skill2"],
            "transferable_skills": ["skill1", "skill2"],
            "learning_path": [
                {{
                    "skill": "skill name",
                    "priority": "high|medium|low",
                    "resources": ["resource1", "resource2"]
                }}
            ]
        }}
    """
        return SYSTEM_PROMPT
    
    