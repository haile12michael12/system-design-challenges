from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .post_entity import PostEntity


class FeedEntity(BaseModel):
    """Feed entity."""
    posts: List[PostEntity]
    user_id: str
    generated_at: datetime = datetime.now()
    page: int = 1
    size: int = 10


class FeedRequestEntity(BaseModel):
    """Feed request entity."""
    user_id: str
    page: int = 1
    size: int = 10
    include_friends_only: bool = True
    include_public_only: bool = True