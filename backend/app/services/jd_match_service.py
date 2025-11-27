import json
import re
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class JDMatchService:
    @staticmethod
    async def match(resume_text: str, analysis_results: dict, job_description: str):

        prompt = f"""
            You are an expert job–resume matching AI.

            Your task is to compare the RESUME TEXT and JOB DESCRIPTION and provide feedback **directly to the user in second-person (you)**.
            
            ❗ STRICT RULES:
            - Never refer to the user as "the candidate", "the person", or "they".
            - Always talk directly to the user using "you", "your skills", "you are missing".
            - Do NOT use third-person language at all.
            - Output MUST be valid JSON only.
            RESUME TEXT:
            {resume_text}

            RESUME ANALYSIS (STRUCTURED):
            {json.dumps(analysis_results, indent=2, default=str)}

            JOB DESCRIPTION:
            {job_description}

            Provide ONLY valid JSON in this strict format:

            ```json
            {{
              "match_percentage": number,
              "matching_skills": [],
              "missing_skills": [],
              "alignment_summary": "",
              "suggested_improvements": []
            }}
        """
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )

        raw = response.choices[0].message.content.strip()
        match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
        json_text = match.group(1) if match else raw

        try:
            return json.loads(json_text)
        except Exception:
            return {
                "match_percentage": 0,
                "matching_skills": [],
                "missing_skills": [],
                "alignment_summary": "Could not parse AI response.",
                "suggested_improvements": []
            }
