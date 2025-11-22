from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserEntity(BaseModel):
    """User entity."""
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class UserCreateEntity(BaseModel):
    """User creation entity."""
    username: str
    email: EmailStr
    password: str


class UserUpdateEntity(BaseModel):
    """User update entity."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserFollowEntity(BaseModel):
    """User follow entity."""
    follower_id: str
    followed_id: str
    created_at: datetime = datetime.now()