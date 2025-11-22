from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class PostEntity(BaseModel):
    """Post entity."""
    id: str
    user_id: str
    content: str
    is_published: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class PostCreateEntity(BaseModel):
    """Post creation entity."""
    user_id: str
    content: str
    is_published: bool = True


class PostUpdateEntity(BaseModel):
    """Post update entity."""
    content: Optional[str] = None
    is_published: Optional[bool] = None