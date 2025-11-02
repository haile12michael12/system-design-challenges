"""Authentication API endpoints"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# Placeholder for user storage (in a real app, this would be a database)
users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S",  # "password"
        "is_active": True,
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00"
    }
}

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate user and return access token"""
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """Register a new user"""
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # In a real app, hash the password
    user_data = user.dict()
    user_data["id"] = len(users_db) + 1
    user_data["hashed_password"] = "placeholder_hashed_password"
    user_data["is_active"] = True
    user_data["created_at"] = "2025-01-01T00:00:00"
    user_data["updated_at"] = "2025-01-01T00:00:00"
    
    users_db[user.username] = user_data
    return user_data