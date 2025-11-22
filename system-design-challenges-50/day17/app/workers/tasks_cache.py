from celery import current_task
from typing import List

from .celery_app import app
from ..cache.feed_cache import FeedCache
from ..cache.post_cache import PostCache
from ..core.logging_config import logger


@app.task(bind=True)
def cache_invalidation_task(self, user_id: str, post_id: str = None) -> dict:
    """
    Task to invalidate cache for a user or specific post.
    
    Args:
        user_id: User ID
        post_id: Optional post ID
        
    Returns:
        dict: Task result
    """
    try:
        logger.info(f"Starting cache invalidation for user {user_id}, post {post_id}")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "initializing"})
        
        if post_id:
            # Invalidate specific post cache
            post_cache = PostCache()
            success = post_cache.invalidate_post(post_id)
            logger.info(f"Post cache invalidation for {post_id}: {'success' if success else 'failed'}")
        else:
            # Invalidate user's feed cache
            feed_cache = FeedCache()
            success = feed_cache.invalidate_feed(user_id)
            logger.info(f"Feed cache invalidation for user {user_id}: {'success' if success else 'failed'}")
        
        result = {
            "status": "completed",
            "user_id": user_id,
            "post_id": post_id,
            "success": success
        }
        
        logger.info(f"Cache invalidation completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in cache invalidation task: {e}")
        return {
            "status": "failed",
            "user_id": user_id,
            "post_id": post_id,
            "error": str(e)
        }


@app.task(bind=True)
def bulk_cache_invalidation_task(self, user_ids: List[str], post_ids: List[str] = None) -> dict:
    """
    Task to invalidate cache for multiple users or posts.
    
    Args:
        user_ids: List of user IDs
        post_ids: Optional list of post IDs
        
    Returns:
        dict: Task result
    """
    try:
        logger.info(f"Starting bulk cache invalidation for {len(user_ids)} users, {len(post_ids) if post_ids else 0} posts")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "initializing", "processed": 0, "total": len(user_ids)})
        
        success_count = 0
        failure_count = 0
        
        if post_ids:
            # Invalidate specific posts cache
            post_cache = PostCache()
            for i, post_id in enumerate(post_ids):
                try:
                    success = post_cache.invalidate_post(post_id)
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                    
                    # Update task state
                    self.update_state(
                        state="PROGRESS", 
                        meta={"status": "processing_posts", "processed": i + 1, "total": len(post_ids)}
                    )
                except Exception as e:
                    logger.error(f"Error invalidating cache for post {post_id}: {e}")
                    failure_count += 1
        else:
            # Invalidate users' feed cache
            feed_cache = FeedCache()
            for i, user_id in enumerate(user_ids):
                try:
                    success = feed_cache.invalidate_feed(user_id)
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                    
                    # Update task state
                    self.update_state(
                        state="PROGRESS", 
                        meta={"status": "processing_users", "processed": i + 1, "total": len(user_ids)}
                    )
                except Exception as e:
                    logger.error(f"Error invalidating cache for user {user_id}: {e}")
                    failure_count += 1
        
        result = {
            "status": "completed",
            "users_processed": len(user_ids),
            "posts_processed": len(post_ids) if post_ids else 0,
            "success_count": success_count,
            "failure_count": failure_count
        }
        
        logger.info(f"Bulk cache invalidation completed: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in bulk cache invalidation task: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }