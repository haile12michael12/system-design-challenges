from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.feed import FeedItem
from app.services.post_service import create_post, get_post, update_post, delete_post
from app.db.session import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=FeedItem, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post_data: dict,  # Simplified for now
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return create_post(db, post_data, current_user["user_id"])

@router.get("/{post_id}", response_model=FeedItem)
async def read_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=FeedItem)
async def update_existing_post(
    post_id: int,
    post_data: dict,  # Simplified for now
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    post = update_post(db, post_id, post_data, current_user["user_id"])
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = delete_post(db, post_id, current_user["user_id"])
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")