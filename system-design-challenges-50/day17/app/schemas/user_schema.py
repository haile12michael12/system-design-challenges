from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for User."""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email")


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpassword"
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    email: Optional[EmailStr] = Field(None, description="User email")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="User password")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johnsmith",
                "email": "johnsmith@example.com",
                "password": "newsecretpassword"
            }
        }


class UserResponse(UserBase):
    """Schema for user response."""
    id: str = Field(..., description="User ID")
    is_active: bool = Field(True, description="Whether the user is active")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "johndoe",
                "email": "john@example.com",
                "is_active": True,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }


class UserFollow(BaseModel):
    """Schema for user follow/unfollow actions."""
    target_user_id: str = Field(..., description="ID of the user to follow/unfollow")
    
    class Config:
        schema_extra = {
            "example": {
                "target_user_id": "550e8400-e29b-41d4-a716-446655440001"
            }
        }