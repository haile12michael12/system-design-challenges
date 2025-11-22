from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..schemas.post_schema import PostCreate, PostResponse
from ..domain.services.feed_writer import FeedWriterService
from ..db.repositories.post_repo import PostRepository
from ..cache.post_cache import PostCache
from ..message_bus.event_publisher import EventPublisher

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    """Create a new post."""
    # In a real implementation, we would:
    # 1. Validate the user
    # 2. Save the post to the database
    # 3. Publish a PostCreated event
    # 4. Return the created post
    
    # Mock implementation for now
    return PostResponse(
        id=1,
        user_id=post.user_id,
        content=post.content,
        created_at="2023-01-01T00:00:00Z"
    )


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    """Delete a post."""
    # In a real implementation, we would:
    # 1. Validate the user owns the post
    # 2. Delete the post from the database
    # 3. Publish a PostDeleted event
    # 4. Invalidate caches
    
    return {"message": f"Post {post_id} deleted"}