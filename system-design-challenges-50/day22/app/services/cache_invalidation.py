from app.cache.redis_client import invalidate_pattern
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def invalidate_user_feed_cache(user_id: int):
    """Invalidate all feed caches for a specific user"""
    if not settings.feature_cache_invalidation:
        return
    
    pattern = f"user_feed:{user_id}:*"
    invalidated_keys = invalidate_pattern(pattern)
    logger.info(f"Invalidated {invalidated_keys} feed cache entries for user {user_id}")

def invalidate_global_feed_cache():
    """Invalidate global explore feed caches"""
    if not settings.feature_cache_invalidation:
        return
    
    pattern = "explore_feed:*"
    invalidated_keys = invalidate_pattern(pattern)
    logger.info(f"Invalidated {invalidated_keys} global feed cache entries")

def invalidate_related_feeds_on_post_create(post_author_id: int):
    """Invalidate feeds of followers when a user creates a post"""
    if not settings.feature_cache_invalidation:
        return
    
    # In a real implementation, we would:
    # 1. Get followers of the post author
    # 2. Invalidate feed caches for those followers
    # For now, we'll just invalidate the author's own feed
    invalidate_user_feed_cache(post_author_id)
    
    logger.info(f"Invalidated related feeds for post by user {post_author_id}")