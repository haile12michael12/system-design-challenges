from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
import logging

from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post_service import PostService
from app.core.security import get_current_user

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new post"""
    try:
        logger.info(f"Creating post for user {current_user['id']}")
        post_service = PostService()
        created_post = await post_service.create_post(post, current_user["id"])
        return created_post
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    """Get a specific post by ID"""
    try:
        logger.info(f"Fetching post {post_id}")
        post_service = PostService()
        post = await post_service.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch post"
        )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a post"""
    try:
        logger.info(f"Updating post {post_id} for user {current_user['id']}")
        post_service = PostService()
        updated_post = await post_service.update_post(post_id, post_update, current_user["id"])
        if not updated_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized"
            )
        return updated_post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a post"""
    try:
        logger.info(f"Deleting post {post_id} for user {current_user['id']}")
        post_service = PostService()
        success = await post_service.delete_post(post_id, current_user["id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )


@router.post("/{post_id}/media")
async def upload_post_media(
    post_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload media for a post"""
    try:
        logger.info(f"Uploading media for post {post_id} by user {current_user['id']}")
        post_service = PostService()
        media_url = await post_service.upload_post_media(post_id, file, current_user["id"])
        if not media_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or unauthorized"
            )
        return {"media_url": media_url}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading media for post {post_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload media"
        )