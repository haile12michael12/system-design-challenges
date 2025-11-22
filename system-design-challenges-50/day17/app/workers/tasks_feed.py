from celery import current_task
from typing import List
import asyncio

from .celery_app import app
from ..domain.entities.post_entity import PostEntity
from ..cache.feed_cache import FeedCache
from ..core.logging_config import logger


@app.task(bind=True)
def feed_propagation_task(self, post_data: dict, follower_ids: List[str]) -> dict:
    """
    Task to propagate a new post to followers' feeds.
    
    Args:
        post_data: Post data
        follower_ids: List of follower IDs
        
    Returns:
        dict: Task result
    """
    try:
        logger.info(f"Starting feed propagation for post {post_data.get('id')} to {len(follower_ids)} followers")
        
        # Convert post data to entity
        post = PostEntity(**post_data)
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"current": 0, "total": len(follower_ids)})
        
        # Propagate to each follower's feed
        success_count = 0
        for i, follower_id in enumerate(follower_ids):
            try:
                # In a real implementation, you would update the follower's feed
                # For now, we'll just simulate the process
                logger.info(f"Propagating post {post.id} to follower {follower_id}")
                
                # Update task state
                self.update_state(
                    state="PROGRESS", 
                    meta={"current": i + 1, "total": len(follower_ids), "follower_id": follower_id}
                )
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"Error propagating post to follower {follower_id}: {e}")
        
        result = {
            "status": "completed",
            "post_id": post.id,
            "followers_processed": len(follower_ids),
            "success_count": success_count,
            "failure_count": len(follower_ids) - success_count
        }
        
        logger.info(f"Feed propagation completed for post {post.id}: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in feed propagation task: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }


@app.task(bind=True)
def update_user_feed_task(self, user_id: str, new_post_id: str) -> dict:
    """
    Task to update a user's feed with a new post.
    
    Args:
        user_id: User ID
        new_post_id: New post ID
        
    Returns:
        dict: Task result
    """
    try:
        logger.info(f"Updating feed for user {user_id} with new post {new_post_id}")
        
        # In a real implementation, you would:
        # 1. Get the user's feed
        # 2. Add the new post to the feed
        # 3. Update the cache
        # 4. Handle any errors
        
        # Simulate the process
        logger.info(f"Feed updated for user {user_id} with post {new_post_id}")
        
        return {
            "status": "completed",
            "user_id": user_id,
            "post_id": new_post_id
        }
        
    except Exception as e:
        logger.error(f"Error updating feed for user {user_id}: {e}")
        return {
            "status": "failed",
            "user_id": user_id,
            "error": str(e)
        }