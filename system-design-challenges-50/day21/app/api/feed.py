from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
import logging

from app.schemas.feed import FeedResponse, FeedItem
from app.services.feed_service import FeedService
from app.core.security import get_current_user
from app.utils.pagination import Pagination

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.get("/", response_model=FeedResponse)
async def get_feed(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get user's personalized feed"""
    try:
        logger.info(f"Fetching feed for user {current_user['id']}, page={page}, size={size}")
        feed_service = FeedService()
        
        # Get paginated feed
        pagination = Pagination(page=page, size=size)
        feed_items, total_count = await feed_service.get_user_feed(current_user["id"], pagination)
        
        return FeedResponse(
            items=feed_items,
            page=page,
            size=size,
            total=total_count
        )
    except Exception as e:
        logger.error(f"Error fetching feed for user {current_user['id']}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch feed"
        )


@router.get("/explore", response_model=FeedResponse)
async def get_explore_feed(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get explore feed with trending content"""
    try:
        logger.info(f"Fetching explore feed for user {current_user['id']}, page={page}, size={size}")
        feed_service = FeedService()
        
        # Get paginated explore feed
        pagination = Pagination(page=page, size=size)
        feed_items, total_count = await feed_service.get_explore_feed(pagination)
        
        return FeedResponse(
            items=feed_items,
            page=page,
            size=size,
            total=total_count
        )
    except Exception as e:
        logger.error(f"Error fetching explore feed for user {current_user['id']}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch explore feed"
        )


@router.post("/{post_id}/like")
async def like_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Like a post"""
    try:
        logger.info(f"User {current_user['id']} liking post {post_id}")
        feed_service = FeedService()
        success = await feed_service.like_post(current_user["id"], post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return {"message": "Successfully liked post"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to like post"
        )


@router.post("/{post_id}/unlike")
async def unlike_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Unlike a post"""
    try:
        logger.info(f"User {current_user['id']} unliking post {post_id}")
        feed_service = FeedService()
        success = await feed_service.unlike_post(current_user["id"], post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return {"message": "Successfully unliked post"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unliking post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unlike post"
        )


@router.post("/{post_id}/bookmark")
async def bookmark_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Bookmark a post"""
    try:
        logger.info(f"User {current_user['id']} bookmarking post {post_id}")
        feed_service = FeedService()
        success = await feed_service.bookmark_post(current_user["id"], post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return {"message": "Successfully bookmarked post"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error bookmarking post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bookmark post"
        )


@router.post("/{post_id}/unbookmark")
async def unbookmark_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove bookmark from a post"""
    try:
        logger.info(f"User {current_user['id']} unbookmarking post {post_id}")
        feed_service = FeedService()
        success = await feed_service.unbookmark_post(current_user["id"], post_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return {"message": "Successfully removed bookmark"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unbookmarking post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove bookmark"
        )