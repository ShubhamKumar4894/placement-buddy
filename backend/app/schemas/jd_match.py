from pydantic import BaseModel

class JDMatchRequest(BaseModel):
    analysis_id: str
    job_description: str
