"""
Feed Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.post_schema import PostResponse
from app.services.feed_service import get_user_feed

router = APIRouter()

class FeedResponse(BaseModel):
    posts: List[PostResponse]
    next_cursor: Optional[str] = None

@router.get("/", response_model=FeedResponse)
async def get_feed(user_id: str, limit: int = 10, cursor: Optional[str] = None):
    """Get user's feed"""
    try:
        feed_data = await get_user_feed(user_id, limit, cursor)
        return FeedResponse(**feed_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))