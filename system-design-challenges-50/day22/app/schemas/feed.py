from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FeedItem(BaseModel):
    id: int
    author_id: int
    content: str
    media_url: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime

class FeedResponse(BaseModel):
    items: List[FeedItem]
    next_cursor: Optional[str] = None
    has_more: bool = False

class ExploreFeedRequest(BaseModel):
    limit: int = 20
    offset: int = 0

class PersonalizedFeedRequest(BaseModel):
    user_id: int
    limit: int = 20
    cursor: Optional[str] = None