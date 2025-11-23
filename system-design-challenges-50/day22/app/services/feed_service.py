from typing import List, Dict, Any
from app.schemas.feed import FeedResponse, ExploreFeedRequest, PersonalizedFeedRequest
from app.cache.redis_client import get_cached_feed, set_cached_feed
from app.models.feed_cache import FeedCache
from sqlalchemy.orm import Session
import json

def get_personalized_feed(db: Session, request: PersonalizedFeedRequest) -> FeedResponse:
    """Get personalized feed for a user with caching"""
    # Try to get from cache first
    cached_feed = get_cached_feed(f"user_feed:{request.user_id}:{request.cursor or 'initial'}")
    if cached_feed:
        return FeedResponse(**json.loads(cached_feed))
    
    # In a real implementation, this would query the database
    # and apply personalization algorithms
    feed_items = []
    
    # Cache the result
    feed_response = FeedResponse(items=feed_items)
    set_cached_feed(
        f"user_feed:{request.user_id}:{request.cursor or 'initial'}",
        json.dumps(feed_response.dict())
    )
    
    return feed_response

def get_explore_feed(db: Session, request: ExploreFeedRequest) -> FeedResponse:
    """Get explore feed (trending content)"""
    # Try to get from cache first
    cached_feed = get_cached_feed(f"explore_feed:{request.offset}")
    if cached_feed:
        return FeedResponse(**json.loads(cached_feed))
    
    # In a real implementation, this would query the database
    # and apply trending algorithms
    feed_items = []
    
    # Cache the result
    feed_response = FeedResponse(items=feed_items)
    set_cached_feed(
        f"explore_feed:{request.offset}",
        json.dumps(feed_response.dict())
    )
    
    return feed_response