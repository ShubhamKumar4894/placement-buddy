from pydantic_settings import BaseSettings
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent   
class Settings(BaseSettings):
    APP_NAME: str = "ResumeFeedback"
    MONGODB_URI: str
    SECRET_KEY: str="supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    UPLOAD_DIR: str = str(PROJECT_ROOT) 
    OPENAI_API_KEY: str | None = None
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
