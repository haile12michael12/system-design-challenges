"""
Cache Invalidation
"""
from app.cache.redis_client import redis_client
from typing import List

async def invalidate_item_cache(item_id: int) -> bool:
    """Invalidate cache for a specific item"""
    # Delete item cache
    await redis_client.delete(f"item:{item_id}")
    # Delete related caches (e.g., lists)
    await redis_client.delete("items:list")
    return True

async def invalidate_all_items_cache() -> bool:
    """Invalidate all items cache"""
    # This is a simplified implementation
    # In a real system, you might want to use Redis SCAN command
    # or maintain a separate index of item keys
    await redis_client.delete("items:list")
    return True

async def invalidate_user_cache(user_id: int) -> bool:
    """Invalidate cache for a specific user"""
    await redis_client.delete(f"user:{user_id}")
    return True