from fastapi import APIRouter, Depends, Query
from typing import List

from ..domain.services.feed_reader import FeedReaderService
from ..schemas.feed_schema import FeedResponse
from ..schemas.post_schema import PostResponse
from ..utils.pagination import PaginationParams

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/", response_model=FeedResponse)
async def get_feed(
    pagination: PaginationParams = Depends(),
    feed_reader: FeedReaderService = Depends(FeedReaderService)
) -> FeedResponse:
    """
    Get user's feed with pagination.
    
    Args:
        pagination: Pagination parameters
        feed_reader: Feed reader service instance
        
    Returns:
        FeedResponse: User's feed data
    """
    posts = await feed_reader.get_feed(pagination.page, pagination.size)
    return FeedResponse(posts=posts, page=pagination.page, size=pagination.size)


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    feed_reader: FeedReaderService = Depends(FeedReaderService)
) -> PostResponse:
    """
    Get a specific post by ID.
    
    Args:
        post_id: Post ID
        feed_reader: Feed reader service instance
        
    Returns:
        PostResponse: Post data
    """
    post = await feed_reader.get_post(post_id)
    return PostResponse(**post)