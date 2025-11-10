"""
User-related Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.schemas.user_schema import UserResponse, UserCreate
from app.services.user_service import get_user, follow_user, unfollow_user

router = APIRouter()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: str):
    """Get user by ID"""
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/{user_id}/follow/{target_user_id}")
async def follow_user_endpoint(user_id: str, target_user_id: str):
    """Follow a user"""
    success = await follow_user(user_id, target_user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to follow user")
    return {"message": f"Successfully followed user {target_user_id}"}

@router.post("/{user_id}/unfollow/{target_user_id}")
async def unfollow_user_endpoint(user_id: str, target_user_id: str):
    """Unfollow a user"""
    success = await unfollow_user(user_id, target_user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to unfollow user")
    return {"message": f"Successfully unfollowed user {target_user_id}"}