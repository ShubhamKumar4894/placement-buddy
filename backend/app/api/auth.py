from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.services.auth_services import register_user, authenticate_user

router = APIRouter()

class RegisterIn(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(payload: RegisterIn):
    try:
        user= await register_user(payload.email, payload.password, payload.full_name)
        return {"message": "User registered successfully","id": str(user.id), "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(payload: LoginIn):
    user= await authenticate_user(payload.email, payload.password)
    return user