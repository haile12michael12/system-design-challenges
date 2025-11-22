import redis
import json
from typing import Optional, Any

from ..core.config import settings
from ..core.logging_config import logger


class RedisClient:
    """Redis client wrapper."""
    
    def __init__(self):
        self.client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )
    
    def get(self, key: str) -> Optional[str]:
        """
        Get value by key.
        
        Args:
            key: Cache key
            
        Returns:
            str: Cached value or None if not found
        """
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None
    
    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """
        Set key-value pair in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            return self.client.set(key, value, ex=expire)
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if successful
        """
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if key exists
        """
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking key {key} existence in Redis: {e}")
            return False


# Global Redis client instance
_redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """
    Get Redis client instance.
    
    Returns:
        RedisClient: Redis client instance
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
    return _redis_client