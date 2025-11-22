from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from .post_schema import PostResponse
from ..utils.pagination import PaginatedResponse


class FeedResponse(PaginatedResponse):
    """Schema for feed response."""
    posts: List[PostResponse] = Field(..., description="List of posts in the feed")
    
    class Config:
        schema_extra = {
            "example": {
                "page": 1,
                "size": 10,
                "total": 100,
                "pages": 10,
                "posts": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "user_id": "550e8400-e29b-41d4-a716-446655440001",
                        "content": "This is my first post!",
                        "is_published": True,
                        "created_at": "2023-01-01T12:00:00Z",
                        "updated_at": "2023-01-01T12:00:00Z"
                    }
                ]
            }
        }