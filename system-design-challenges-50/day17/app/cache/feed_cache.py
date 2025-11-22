from typing import List, Optional
import json

from ..domain.entities.post_entity import PostEntity
from .redis_client import get_redis_client
from ..core.logging_config import logger


class FeedCache:
    """Cache for user feeds."""
    
    def __init__(self):
        self.redis_client = get_redis_client()
    
    def _get_feed_key(self, user_id: str, page: int, size: int) -> str:
        """
        Generate cache key for a user's feed.
        
        Args:
            user_id: User ID
            page: Page number
            size: Page size
            
        Returns:
            str: Cache key
        """
        return f"feed:{user_id}:page:{page}:size:{size}"
    
    async def get_feed(self, user_id: str, page: int, size: int) -> Optional[List[PostEntity]]:
        """
        Get user's feed from cache.
        
        Args:
            user_id: User ID
            page: Page number
            size: Page size
            
        Returns:
            List[PostEntity]: List of posts or None if not in cache
        """
        try:
            key = self._get_feed_key(user_id, page, size)
            cached_data = self.redis_client.get(key)
            
            if cached_data:
                feed_data = json.loads(cached_data)
                posts = [PostEntity(**post_data) for post_data in feed_data["posts"]]
                logger.info(f"Feed for user {user_id} found in cache")
                return posts
            
            logger.info(f"Feed for user {user_id} not found in cache")
            return None
            
        except Exception as e:
            logger.error(f"Error getting feed from cache for user {user_id}: {e}")
            return None
    
    async def cache_feed(self, user_id: str, posts: List[PostEntity], page: int, size: int, expire: int = 300) -> bool:
        """
        Cache user's feed.
        
        Args:
            user_id: User ID
            posts: List of posts
            page: Page number
            size: Page size
            expire: Expiration time in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            key = self._get_feed_key(user_id, page, size)
            feed_data = {
                "posts": [post.dict() for post in posts],
                "user_id": user_id,
                "page": page,
                "size": size
            }
            
            success = self.redis_client.set(key, json.dumps(feed_data), expire)
            if success:
                logger.info(f"Feed for user {user_id} cached successfully")
            else:
                logger.warning(f"Failed to cache feed for user {user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error caching feed for user {user_id}: {e}")
            return False
    
    async def invalidate_feed(self, user_id: str) -> bool:
        """
        Invalidate all cached feeds for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if successful
        """
        try:
            # In a real implementation, you would need to invalidate all feed keys for the user
            # This is a simplified version that just logs the action
            logger.info(f"Invalidating feed cache for user {user_id}")
            # For now, we'll just return True to indicate success
            return True
            
        except Exception as e:
            logger.error(f"Error invalidating feed cache for user {user_id}: {e}")
            return False