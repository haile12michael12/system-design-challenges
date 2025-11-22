from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PostBase(BaseModel):
    """Base schema for Post."""
    content: str = Field(..., min_length=1, max_length=1000, description="Post content")


class PostCreate(PostBase):
    """Schema for creating a post."""
    is_published: bool = Field(True, description="Whether the post is published")
    
    class Config:
        schema_extra = {
            "example": {
                "content": "This is my first post!",
                "is_published": True
            }
        }


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    content: Optional[str] = Field(None, min_length=1, max_length=1000, description="Post content")
    is_published: Optional[bool] = Field(None, description="Whether the post is published")
    
    class Config:
        schema_extra = {
            "example": {
                "content": "This is my updated post!",
                "is_published": True
            }
        }


class PostResponse(PostBase):
    """Schema for post response."""
    id: str = Field(..., description="Post ID")
    user_id: str = Field(..., description="User ID")
    is_published: bool = Field(..., description="Whether the post is published")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "550e8400-e29b-41d4-a716-446655440001",
                "content": "This is my first post!",
                "is_published": True,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-01T12:00:00Z"
            }
        }