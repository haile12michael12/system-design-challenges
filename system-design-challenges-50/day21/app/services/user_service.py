from typing import Optional, List, Dict
import logging
from datetime import datetime

from app.repositories.user_repo import UserRepository
from app.repositories.follow_repo import FollowRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.caching import cache_get, cache_set, cache_delete
from app.core.security import hash_password


def model_to_dict(model) -> Dict:
    """Convert SQLAlchemy model to dictionary"""
    if model is None:
        return None
    
    # For testing purposes, we'll create a simple dict representation
    # In a real implementation, this would extract actual model attributes
    return {
        "id": getattr(model, 'id', ''),
        "username": getattr(model, 'username', ''),
        "email": getattr(model, 'email', ''),
        "full_name": getattr(model, 'full_name', None),
        "bio": getattr(model, 'bio', None),
        "created_at": getattr(model, 'created_at', datetime.utcnow()),
        "updated_at": getattr(model, 'updated_at', datetime.utcnow())
    }

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.follow_repo = FollowRepository()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        try:
            logger.info(f"Creating user {user_data.username}")
            
            # Hash the password
            hashed_password = hash_password(user_data.password)
            user_data.password = hashed_password
            
            # Create user in database
            user = await self.user_repo.create_user(user_data)
            
            # Cache the user
            cache_key = f"user:{user.id}"
            await cache_set(cache_key, model_to_dict(user), expire=3600)  # Cache for 1 hour
            
            return UserResponse(**model_to_dict(user))
        except Exception as e:
            logger.error(f"Error creating user {user_data.username}: {e}")
            raise

    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by ID"""
        try:
            logger.info(f"Fetching user {user_id}")
            
            # Try to get from cache first
            cache_key = f"user:{user_id}"
            cached_user = await cache_get(cache_key)
            if cached_user:
                logger.info(f"User {user_id} found in cache")
                return UserResponse(**cached_user)
            
            # Get from database
            user = await self.user_repo.get_user(user_id)
            if not user:
                return None
            
            # Cache the user
            await cache_set(cache_key, model_to_dict(user), expire=3600)  # Cache for 1 hour
            
            return UserResponse(**model_to_dict(user))
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            raise

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
        """Update a user"""
        try:
            logger.info(f"Updating user {user_id}")
            
            # If password is being updated, hash it
            if user_data.password:
                user_data.password = hash_password(user_data.password)
            
            # Update user in database
            updated_user = await self.user_repo.update_user(user_id, user_data)
            if not updated_user:
                return None
            
            # Update cache
            cache_key = f"user:{user_id}"
            await cache_set(cache_key, model_to_dict(updated_user), expire=3600)
            
            return UserResponse(**model_to_dict(updated_user))
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            logger.info(f"Deleting user {user_id}")
            
            # Delete user from database
            success = await self.user_repo.delete_user(user_id)
            if not success:
                return False
            
            # Delete from cache
            cache_key = f"user:{user_id}"
            await cache_delete(cache_key)
            
            # Delete follow relationships
            await self.follow_repo.delete_user_follows(user_id)
            
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise

    async def follow_user(self, follower_id: str, following_id: str) -> bool:
        """Follow a user"""
        try:
            logger.info(f"User {follower_id} following user {following_id}")
            
            # Check if users exist
            follower = await self.get_user(follower_id)
            following = await self.get_user(following_id)
            
            if not follower or not following:
                return False
            
            # Create follow relationship
            success = await self.follow_repo.create_follow(follower_id, following_id)
            if not success:
                return False
            
            # Invalidate follower's feed cache
            await cache_delete(f"user_feed:{follower_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error following user {following_id}: {e}")
            raise

    async def unfollow_user(self, follower_id: str, following_id: str) -> bool:
        """Unfollow a user"""
        try:
            logger.info(f"User {follower_id} unfollowing user {following_id}")
            
            # Delete follow relationship
            success = await self.follow_repo.delete_follow(follower_id, following_id)
            if not success:
                return False
            
            # Invalidate follower's feed cache
            await cache_delete(f"user_feed:{follower_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error unfollowing user {following_id}: {e}")
            raise