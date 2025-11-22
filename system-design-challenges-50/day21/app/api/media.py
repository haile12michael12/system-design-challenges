from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
import logging

from app.services.media_service import MediaService
from app.core.security import get_current_user

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload media file"""
    try:
        logger.info(f"Uploading media for user {current_user['id']}")
        media_service = MediaService()
        media_url = await media_service.upload_media(file, current_user["id"])
        return {"media_url": media_url}
    except Exception as e:
        logger.error(f"Error uploading media: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload media"
        )


@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete media file"""
    try:
        logger.info(f"Deleting media {media_id} for user {current_user['id']}")
        media_service = MediaService()
        success = await media_service.delete_media(media_id, current_user["id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Media not found or unauthorized"
            )
        return {"message": "Successfully deleted media"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting media {media_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete media"
        )


@router.get("/{media_id}/info")
async def get_media_info(
    media_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get media file information"""
    try:
        logger.info(f"Fetching media info {media_id} for user {current_user['id']}")
        media_service = MediaService()
        media_info = await media_service.get_media_info(media_id)
        if not media_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Media not found"
            )
        return media_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching media info {media_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch media info"
        )


@router.post("/{media_id}/process")
async def process_media(
    media_id: str,
    transformations: List[str],
    current_user: dict = Depends(get_current_user)
):
    """Process media file with specified transformations"""
    try:
        logger.info(f"Processing media {media_id} for user {current_user['id']}")
        media_service = MediaService()
        processed_urls = await media_service.process_media(media_id, transformations, current_user["id"])
        if not processed_urls:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Media not found or unauthorized"
            )
        return {"processed_urls": processed_urls}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing media {media_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process media"
        )