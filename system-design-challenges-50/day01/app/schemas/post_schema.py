"""
Pydantic Models for Posts
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    caption: str
    image_url: str
    user_id: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    caption: Optional[str] = None

class PostResponse(PostBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True