from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.config import settings
from app.models.user import User
from app.services.auth_service import verify_password
from typing import Optional
import redis

# Redis client for dependencies
redis_client = redis.Redis.from_url(settings.redis_url)

async def get_current_user(token: str) -> dict:
    """Dependency to get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"user_id": user_id}

async def get_redis():
    """Dependency to get Redis client"""
    return redis_client

async def rate_limiter(user_id: str, limit: int = 100, window: int = 60):
    """Rate limiting dependency"""
    key = f"rate_limit:{user_id}"
    current = redis_client.get(key)
    
    if current is None:
        redis_client.setex(key, window, 1)
        return True
    
    if int(current) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    redis_client.incr(key)
    return True