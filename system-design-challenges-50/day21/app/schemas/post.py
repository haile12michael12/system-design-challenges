from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    content: str
    media_url: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None


class PostResponse(PostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime
    likes_count: int
    comments_count: int

    class Config:
        from_attributes = True