from app.cache.redis_client import redis_client
from app.config import settings
from typing import Optional
import time

class RateLimiter:
    """Rate limiting utility using Redis"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """
        Check if an action is allowed based on rate limiting rules
        
        Args:
            key: Unique identifier for the rate limit (e.g., user_id:action)
            limit: Maximum number of requests allowed
            window: Time window in seconds
            
        Returns:
            bool: True if allowed, False if rate limited
        """
        try:
            # Use Redis sliding window counter
            current_time = int(time.time())
            window_start = current_time - window
            
            # Remove old entries
            self.redis.zremrangebyscore(key, 0, window_start)
            
            # Check current count
            current_count = self.redis.zcard(key)
            
            if current_count >= limit:
                return False
            
            # Add current request
            self.redis.zadd(key, {str(current_time): current_time})
            self.redis.expire(key, window)
            
            return True
        except Exception:
            # Fail open - allow request if Redis is unavailable
            return True
    
    def get_retry_after(self, key: str, window: int) -> Optional[int]:
        """Get seconds until rate limit resets"""
        try:
            current_time = int(time.time())
            window_start = current_time - window
            
            # Remove old entries
            self.redis.zremrangebyscore(key, 0, window_start)
            
            # Get oldest entry
            oldest = self.redis.zrange(key, 0, 0, withscores=True)
            if oldest:
                oldest_time = int(oldest[0][1])
                return max(0, (oldest_time + window) - current_time)
            
            return None
        except Exception:
            return None

# Global rate limiter instance
rate_limiter = RateLimiter(redis_client)

def throttle_user_action(user_id: int, action: str, limit: int = 100, window: int = 60) -> bool:
    """
    Throttle a user action
    
    Args:
        user_id: User identifier
        action: Action being performed
        limit: Maximum requests allowed
        window: Time window in seconds
        
    Returns:
        bool: True if allowed, False if rate limited
    """
    key = f"throttle:{user_id}:{action}"
    return rate_limiter.is_allowed(key, limit, window)