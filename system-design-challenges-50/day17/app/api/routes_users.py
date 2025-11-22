from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..schemas.user_schema import UserCreate, UserResponse, UserFollow
from ..domain.services.feed_writer import FeedWriterService
from ..domain.services.feed_reader import FeedReaderService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    feed_writer: FeedWriterService = Depends(FeedWriterService)
) -> UserResponse:
    """
    Create a new user.
    
    Args:
        user: User creation data
        feed_writer: Feed writer service instance
        
    Returns:
        UserResponse: Created user data
    """
    try:
        created_user = await feed_writer.create_user(user.dict())
        return UserResponse(**created_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/follow", response_model=dict)
async def follow_user(
    user_id: str,
    follow_data: UserFollow,
    feed_writer: FeedWriterService = Depends(FeedWriterService)
) -> dict:
    """
    Follow another user.
    
    Args:
        user_id: User ID of the follower
        follow_data: Follow request data
        feed_writer: Feed writer service instance
        
    Returns:
        dict: Success message
    """
    try:
        await feed_writer.follow_user(user_id, follow_data.target_user_id)
        return {"message": f"Successfully followed user {follow_data.target_user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/unfollow", response_model=dict)
async def unfollow_user(
    user_id: str,
    follow_data: UserFollow,
    feed_writer: FeedWriterService = Depends(FeedWriterService)
) -> dict:
    """
    Unfollow a user.
    
    Args:
        user_id: User ID of the follower
        follow_data: Unfollow request data
        feed_writer: Feed writer service instance
        
    Returns:
        dict: Success message
    """
    try:
        await feed_writer.unfollow_user(user_id, follow_data.target_user_id)
        return {"message": f"Successfully unfollowed user {follow_data.target_user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))