"""Service layer for caching"""
import redis
import json
from typing import Optional, Any
from app.core.config import settings

class CacheService:
    """Service class for handling cache operations"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache"""
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception:
            return False