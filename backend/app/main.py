from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.database import init_db
from app.api.auth import router as auth_router
from app.api.resume import router as file_router
app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,                   
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(file_router, prefix="/api/v1/resume", tags=["files"])
@app.on_event("startup")
async def startup_event():
    await init_db()
