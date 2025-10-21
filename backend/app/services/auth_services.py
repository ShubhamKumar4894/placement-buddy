from app.models.user import User
from app.utils.security import hash_password, decode_access_token, create_access_token, verify_password
from typing import Optional
from beanie import PydanticObjectId

async def register_user(email: str, password: str, full_name: Optional[str] = None)->User:
    existing_user= await User.find_one(User.email==email)
    if existing_user:
        raise ValueError("Email already registered")
    hashed_pwd= hash_password(password)
    user = User(email=email, hashed_password=hashed_pwd, full_name=full_name)
    await user.insert()
    return user

async def authenticate_user(email: str, password: str)->Optional[User]:
    user= await User.find_one(User.email==email)
    if not user or not user.hashed_password:
        return {"error": "Invalid credentials"}
    if not verify_password(password, user.hashed_password):
        return {"error": "Invalid Password"}
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}

