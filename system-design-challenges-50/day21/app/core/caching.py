import redis
import json
import logging
from typing import Optional, Any
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def cache_get(key: str) -> Optional[Any]:
    """Get a value from cache"""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Error getting cache key {key}: {e}")
        return None


async def cache_set(key: str, value: Any, expire: int = 3600) -> bool:
    """Set a value in cache"""
    try:
        serialized_value = json.dumps(value, default=str)
        result = redis_client.setex(key, expire, serialized_value)
        return result
    except Exception as e:
        logger.error(f"Error setting cache key {key}: {e}")
        return False


async def cache_delete(key: str) -> bool:
    """Delete a value from cache"""
    try:
        result = redis_client.delete(key)
        return result > 0
    except Exception as e:
        logger.error(f"Error deleting cache key {key}: {e}")
        return False


async def cache_exists(key: str) -> bool:
    """Check if a key exists in cache"""
    try:
        return redis_client.exists(key) > 0
    except Exception as e:
        logger.error(f"Error checking cache key {key}: {e}")
        return False