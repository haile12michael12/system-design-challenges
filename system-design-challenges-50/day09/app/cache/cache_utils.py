"""
Cache Utilities
"""
from app.cache.redis_client import redis_client
import json
from typing import Any, Optional

async def get_from_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    value = await redis_client.get(key)
    if value:
        return json.loads(value)
    return None

async def set_in_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set value in cache with TTL"""
    serialized_value = json.dumps(value)
    return await redis_client.set(key, serialized_value, ex=ttl)

async def delete_from_cache(key: str) -> bool:
    """Delete value from cache"""
    result = await redis_client.delete(key)
    return result > 0

async def invalidate_pattern(pattern: str) -> int:
    """Invalidate all keys matching a pattern"""
    # This is a simplified implementation
    # In a real system, you might want to use Redis SCAN command
    # or maintain a separate index of keys by pattern
    return 0