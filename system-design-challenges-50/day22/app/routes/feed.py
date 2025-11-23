from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.feed import FeedResponse, ExploreFeedRequest, PersonalizedFeedRequest
from app.services.feed_service import get_personalized_feed, get_explore_feed
from app.db.session import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/personalized", response_model=FeedResponse)
async def get_user_feed(
    limit: int = Query(20, ge=1, le=100),
    cursor: str = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    request = PersonalizedFeedRequest(user_id=int(current_user["user_id"]), limit=limit, cursor=cursor)
    return get_personalized_feed(db, request)

@router.get("/explore", response_model=FeedResponse)
async def get_explore_feed_route(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    request = ExploreFeedRequest(limit=limit, offset=offset)
    return get_explore_feed(db, request)