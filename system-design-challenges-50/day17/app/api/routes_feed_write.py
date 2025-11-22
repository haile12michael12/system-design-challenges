from fastapi import APIRouter, Depends, HTTPException
from typing import Any

from ..domain.services.feed_writer import FeedWriterService
from ..schemas.post_schema import PostCreate, PostResponse
from ..core.security import decode_access_token
from ..core.exceptions import UnauthorizedException

router = APIRouter(prefix="/posts", tags=["posts"])


def get_current_user(token: str) -> dict:
    """Get current user from JWT token."""
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Invalid token")
    return payload


@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: dict = Depends(get_current_user),
    feed_writer: FeedWriterService = Depends(FeedWriterService)
) -> PostResponse:
    """
    Create a new post.
    
    Args:
        post: Post creation data
        current_user: Current authenticated user
        feed_writer: Feed writer service instance
        
    Returns:
        PostResponse: Created post data
    """
    try:
        # Add user ID to post data
        post_data = post.dict()
        post_data["user_id"] = current_user["user_id"]
        
        # Create post through service
        created_post = await feed_writer.create_post(post_data)
        return PostResponse(**created_post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))