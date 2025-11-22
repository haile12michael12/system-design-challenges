import redis
import json
from typing import Optional, List, Dict, Any

from ..core.config import settings
from ..core.logging import logger


class CacheService:
    """Cache service for storing and retrieving data."""
    
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
            logger.error(f"Error getting key {key} from cache: {e}")
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
            logger.error(f"Error setting key {key} in cache: {e}")
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
            logger.error(f"Error deleting key {key} from cache: {e}")
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
            logger.error(f"Error checking key {key} existence in cache: {e}")
            return False


# Global cache service instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """
    Get cache service instance.
    
    Returns:
        CacheService: Cache service instance
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service