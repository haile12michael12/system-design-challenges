from typing import Optional, List, Tuple
import logging
from datetime import datetime

from app.repositories.post_repo import PostRepository
from app.repositories.user_repo import UserRepository
from app.repositories.follow_repo import FollowRepository
from app.repositories.feed_repo import FeedRepository
from app.schemas.feed import FeedItem
from app.utils.pagination import Pagination
from app.core.caching import cache_get, cache_set, cache_delete

logger = logging.getLogger(__name__)


class FeedService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.user_repo = UserRepository()
        self.follow_repo = FollowRepository()
        self.feed_repo = FeedRepository()

    async def get_user_feed(self, user_id: str, pagination: Pagination) -> Tuple[List[FeedItem], int]:
        """Get user's personalized feed"""
        try:
            logger.info(f"Fetching feed for user {user_id}")
            
            # Try to get from cache first
            cache_key = f"user_feed:{user_id}:{pagination.page}:{pagination.size}"
            cached_feed = await cache_get(cache_key)
            if cached_feed:
                logger.info(f"Feed for user {user_id} found in cache")
                return cached_feed["items"], cached_feed["total"]
            
            # Get user's following list
            following_ids = await self.follow_repo.get_user_following(user_id)
            
            # Get posts from followed users
            posts, total_count = await self.post_repo.get_posts_by_authors(
                following_ids, pagination
            )
            
            # Convert posts to feed items
            feed_items = [
                FeedItem(
                    id=post.id,
                    author_id=post.author_id,
                    content=post.content,
                    media_url=post.media_url,
                    created_at=post.created_at,
                    likes_count=0,  # In a real implementation, this would come from a likes service
                    comments_count=0  # In a real implementation, this would come from a comments service
                )
                for post in posts
            ]
            
            # Cache the feed
            feed_data = {
                "items": [item.dict() for item in feed_items],
                "total": total_count
            }
            await cache_set(cache_key, feed_data, expire=300)  # Cache for 5 minutes
            
            return feed_items, total_count
        except Exception as e:
            logger.error(f"Error fetching feed for user {user_id}: {e}")
            raise

    async def get_explore_feed(self, pagination: Pagination) -> Tuple[List[FeedItem], int]:
        """Get explore feed with trending content"""
        try:
            logger.info("Fetching explore feed")
            
            # Try to get from cache first
            cache_key = f"explore_feed:{pagination.page}:{pagination.size}"
            cached_feed = await cache_get(cache_key)
            if cached_feed:
                logger.info("Explore feed found in cache")
                return cached_feed["items"], cached_feed["total"]
            
            # Get trending posts (in a real implementation, this would use analytics data)
            posts, total_count = await self.post_repo.get_trending_posts(pagination)
            
            # Convert posts to feed items
            feed_items = [
                FeedItem(
                    id=post.id,
                    author_id=post.author_id,
                    content=post.content,
                    media_url=post.media_url,
                    created_at=post.created_at,
                    likes_count=0,  # In a real implementation, this would come from a likes service
                    comments_count=0  # In a real implementation, this would come from a comments service
                )
                for post in posts
            ]
            
            # Cache the feed
            feed_data = {
                "items": [item.dict() for item in feed_items],
                "total": total_count
            }
            await cache_set(cache_key, feed_data, expire=300)  # Cache for 5 minutes
            
            return feed_items, total_count
        except Exception as e:
            logger.error(f"Error fetching explore feed: {e}")
            raise

    async def like_post(self, user_id: str, post_id: str) -> bool:
        """Like a post"""
        try:
            logger.info(f"User {user_id} liking post {post_id}")
            
            # In a real implementation, this would interact with a likes service
            # For now, we'll just update the post's like count in the database
            success = await self.post_repo.increment_post_likes(post_id)
            if not success:
                return False
            
            # Invalidate post cache
            await cache_delete(f"post:{post_id}")
            
            # Invalidate user's feed cache (likes might affect ranking)
            await cache_delete(f"user_feed:{user_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error liking post {post_id}: {e}")
            raise

    async def unlike_post(self, user_id: str, post_id: str) -> bool:
        """Unlike a post"""
        try:
            logger.info(f"User {user_id} unliking post {post_id}")
            
            # In a real implementation, this would interact with a likes service
            # For now, we'll just update the post's like count in the database
            success = await self.post_repo.decrement_post_likes(post_id)
            if not success:
                return False
            
            # Invalidate post cache
            await cache_delete(f"post:{post_id}")
            
            # Invalidate user's feed cache
            await cache_delete(f"user_feed:{user_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error unliking post {post_id}: {e}")
            raise

    async def bookmark_post(self, user_id: str, post_id: str) -> bool:
        """Bookmark a post"""
        try:
            logger.info(f"User {user_id} bookmarking post {post_id}")
            
            # Add to user's bookmarks
            success = await self.feed_repo.add_bookmark(user_id, post_id)
            if not success:
                return False
            
            # Invalidate user's feed cache (might affect bookmark status display)
            await cache_delete(f"user_feed:{user_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error bookmarking post {post_id}: {e}")
            raise

    async def unbookmark_post(self, user_id: str, post_id: str) -> bool:
        """Remove bookmark from a post"""
        try:
            logger.info(f"User {user_id} unbookmarking post {post_id}")
            
            # Remove from user's bookmarks
            success = await self.feed_repo.remove_bookmark(user_id, post_id)
            if not success:
                return False
            
            # Invalidate user's feed cache
            await cache_delete(f"user_feed:{user_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error unbookmarking post {post_id}: {e}")
            raise