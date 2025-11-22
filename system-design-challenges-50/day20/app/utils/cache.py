import redis
import json
import logging
from typing import Any, Optional
from datetime import timedelta

from app.core.config import settings

# Set up logging
logger = logging.getLogger(__name__)


class CacheService:
    """Redis cache service"""
    
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache"""
        try:
            serialized_value = json.dumps(value, default=str)
            result = self.redis_client.setex(key, expire, serialized_value)
            return result
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def flush(self) -> bool:
        """Flush all cache"""
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")
            return False


# Global cache instance
cache_service = CacheService()


def get_cache_service() -> CacheService:
    """Get cache service instance"""
    return cache_service


def cache_result(expire: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache_service.set(cache_key, result, expire)
            logger.debug(f"Cache set for {cache_key}")
            
            return result
        return wrapper
    return decorator