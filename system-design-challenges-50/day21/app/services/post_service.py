from typing import Optional, List, Dict
import logging
from datetime import datetime

from app.repositories.post_repo import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.caching import cache_get, cache_set, cache_delete


def model_to_dict(model) -> Dict:
    """Convert SQLAlchemy model to dictionary"""
    if model is None:
        return None
    
    # For testing purposes, we'll create a simple dict representation
    # In a real implementation, this would extract actual model attributes
    return {
        "id": getattr(model, 'id', ''),
        "author_id": getattr(model, 'author_id', ''),
        "content": getattr(model, 'content', ''),
        "media_url": getattr(model, 'media_url', None),
        "created_at": getattr(model, 'created_at', datetime.utcnow()),
        "updated_at": getattr(model, 'updated_at', datetime.utcnow()),
        "likes_count": getattr(model, 'likes_count', 0),
        "comments_count": getattr(model, 'comments_count', 0)
    }

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self):
        self.post_repo = PostRepository()

    async def create_post(self, post_data: PostCreate, user_id: str) -> PostResponse:
        """Create a new post"""
        try:
            logger.info(f"Creating post for user {user_id}")
            
            # Create post in database
            post = await self.post_repo.create_post(post_data, user_id)
            
            # Cache the post
            cache_key = f"post:{post.id}"
            await cache_set(cache_key, model_to_dict(post), expire=3600)  # Cache for 1 hour
            
            # Invalidate user's feed cache
            await cache_delete(f"user_feed:{user_id}")
            
            return PostResponse(**model_to_dict(post))
        except Exception as e:
            logger.error(f"Error creating post for user {user_id}: {e}")
            raise

    async def get_post(self, post_id: str) -> Optional[PostResponse]:
        """Get a post by ID"""
        try:
            logger.info(f"Fetching post {post_id}")
            
            # Try to get from cache first
            cache_key = f"post:{post_id}"
            cached_post = await cache_get(cache_key)
            if cached_post:
                logger.info(f"Post {post_id} found in cache")
                return PostResponse(**cached_post)
            
            # Get from database
            post = await self.post_repo.get_post(post_id)
            if not post:
                return None
            
            # Cache the post
            await cache_set(cache_key, model_to_dict(post), expire=3600)  # Cache for 1 hour
            
            return PostResponse(**model_to_dict(post))
        except Exception as e:
            logger.error(f"Error fetching post {post_id}: {e}")
            raise

    async def update_post(self, post_id: str, post_data: PostUpdate, user_id: str) -> Optional[PostResponse]:
        """Update a post"""
        try:
            logger.info(f"Updating post {post_id} for user {user_id}")
            
            # Check if user is authorized to update this post
            existing_post = await self.get_post(post_id)
            if not existing_post or existing_post.author_id != user_id:
                return None
            
            # Update post in database
            updated_post = await self.post_repo.update_post(post_id, post_data)
            if not updated_post:
                return None
            
            # Update cache
            cache_key = f"post:{post_id}"
            await cache_set(cache_key, model_to_dict(updated_post), expire=3600)
            
            # Invalidate user's feed cache
            await cache_delete(f"user_feed:{user_id}")
            
            return PostResponse(**model_to_dict(updated_post))
        except Exception as e:
            logger.error(f"Error updating post {post_id}: {e}")
            raise

    async def delete_post(self, post_id: str, user_id: str) -> bool:
        """Delete a post"""
        try:
            logger.info(f"Deleting post {post_id} for user {user_id}")
            
            # Check if user is authorized to delete this post
            existing_post = await self.get_post(post_id)
            if not existing_post or existing_post.author_id != user_id:
                return False
            
            # Delete post from database
            success = await self.post_repo.delete_post(post_id)
            if not success:
                return False
            
            # Delete from cache
            cache_key = f"post:{post_id}"
            await cache_delete(cache_key)
            
            # Invalidate user's feed cache
            await cache_delete(f"user_feed:{user_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {e}")
            raise

    async def upload_post_media(self, post_id: str, file, user_id: str) -> Optional[str]:
        """Upload media for a post"""
        try:
            logger.info(f"Uploading media for post {post_id} by user {user_id}")
            
            # Check if user is authorized to upload media for this post
            existing_post = await self.get_post(post_id)
            if not existing_post or existing_post.author_id != user_id:
                return None
            
            # In a real implementation, this would upload to a media service
            # For now, we'll just return a placeholder URL
            media_url = f"https://media.example.com/posts/{post_id}/{file.filename}"
            
            # Update post with media URL
            post_update = PostUpdate(media_url=media_url)
            updated_post = await self.update_post(post_id, post_update, user_id)
            
            return media_url if updated_post else None
        except Exception as e:
            logger.error(f"Error uploading media for post {post_id}: {e}")
            raise