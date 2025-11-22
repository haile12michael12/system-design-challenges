from typing import Optional
import json

from ..domain.entities.post_entity import PostEntity
from .redis_client import get_redis_client
from ..core.logging_config import logger


class PostCache:
    """Cache for individual posts."""
    
    def __init__(self):
        self.redis_client = get_redis_client()
    
    def _get_post_key(self, post_id: str) -> str:
        """
        Generate cache key for a post.
        
        Args:
            post_id: Post ID
            
        Returns:
            str: Cache key
        """
        return f"post:{post_id}"
    
    async def get_post(self, post_id: str) -> Optional[PostEntity]:
        """
        Get post from cache.
        
        Args:
            post_id: Post ID
            
        Returns:
            PostEntity: Post or None if not in cache
        """
        try:
            key = self._get_post_key(post_id)
            cached_data = self.redis_client.get(key)
            
            if cached_data:
                post_data = json.loads(cached_data)
                post = PostEntity(**post_data)
                logger.info(f"Post {post_id} found in cache")
                return post
            
            logger.info(f"Post {post_id} not found in cache")
            return None
            
        except Exception as e:
            logger.error(f"Error getting post {post_id} from cache: {e}")
            return None
    
    async def cache_post(self, post: PostEntity, expire: int = 3600) -> bool:
        """
        Cache a post.
        
        Args:
            post: Post to cache
            expire: Expiration time in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            key = self._get_post_key(post.id)
            success = self.redis_client.set(key, json.dumps(post.dict()), expire)
            
            if success:
                logger.info(f"Post {post.id} cached successfully")
            else:
                logger.warning(f"Failed to cache post {post.id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error caching post {post.id}: {e}")
            return False
    
    async def invalidate_post(self, post_id: str) -> bool:
        """
        Invalidate a post in cache.
        
        Args:
            post_id: Post ID
            
        Returns:
            bool: True if successful
        """
        try:
            key = self._get_post_key(post_id)
            success = self.redis_client.delete(key)
            
            if success:
                logger.info(f"Post {post_id} cache invalidated successfully")
            else:
                logger.warning(f"Failed to invalidate cache for post {post_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error invalidating cache for post {post_id}: {e}")
            return False