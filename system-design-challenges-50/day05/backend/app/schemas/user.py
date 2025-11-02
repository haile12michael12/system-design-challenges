"""Pydantic models for users"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str