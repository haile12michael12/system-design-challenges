from fastapi import APIRouter, Query
from typing import List

from ..schemas.feed_schema import FeedResponse
from ..domain.services.feed_reader import FeedReaderService
from ..db.repositories.post_repo import PostRepository
from ..cache.feed_cache import FeedCache

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/", response_model=List[FeedResponse])
async def get_feed(
    user_id: int,
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):
    """Get user's feed."""
    # In a real implementation, we would:
    # 1. Validate the user
    # 2. Check cache first
    # 3. If not in cache, fetch from database
    # 4. Return the feed
    
    # Mock implementation for now
    return [
        FeedResponse(
            id=1,
            user_id=user_id,
            content="Sample post content",
            author="Sample Author",
            created_at="2023-01-01T00:00:00Z"
        )
    ]


@router.get("/timeline", response_model=List[FeedResponse])
async def get_user_timeline(
    user_id: int,
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):
    """Get user's timeline (their own posts)."""
    # In a real implementation, we would:
    # 1. Validate the user
    # 2. Fetch user's posts from database
    # 3. Return the timeline
    
    # Mock implementation for now
    return [
        FeedResponse(
            id=1,
            user_id=user_id,
            content="My post content",
            author="Current User",
            created_at="2023-01-01T00:00:00Z"
        )
    ]