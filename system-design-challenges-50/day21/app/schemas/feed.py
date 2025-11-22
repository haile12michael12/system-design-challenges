from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FeedItem(BaseModel):
    id: str
    author_id: str
    content: str
    media_url: Optional[str] = None
    created_at: datetime
    likes_count: int
    comments_count: int


class FeedResponse(BaseModel):
    items: List[FeedItem]
    page: int
    size: int
    total: int