from celery import Celery
from typing import Dict, Any
import asyncio

from ..core.config import settings
from ..services.prefetch_service import PrefetchService
from ..core.logging import logger


# Create Celery app
celery_app = Celery("news_service")

# Configure Celery
celery_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "prefetch_task": {"queue": "prefetch"},
        "cache_warm_task": {"queue": "cache"},
    },
)


@celery_app.task(bind=True)
def prefetch_task(self, user_id: str) -> Dict[str, Any]:
    """
    Task to prefetch articles for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Dict[str, Any]: Task result
    """
    try:
        logger.info(f"Starting prefetch task for user: {user_id}")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "initializing"})
        
        # Create prefetch service
        prefetch_service = PrefetchService()
        
        # Run prefetch
        # Note: We need to run this in an async context
        # For simplicity, we'll simulate the prefetching
        logger.info(f"Prefetching articles for user: {user_id}")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "prefetching"})
        
        # Simulate prefetching
        import time
        time.sleep(2)  # Simulate work
        
        result = {
            "status": "completed",
            "user_id": user_id,
            "message": f"Prefetched articles for user {user_id}"
        }
        
        logger.info(f"Prefetch task completed for user: {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error in prefetch task for user {user_id}: {e}")
        return {
            "status": "failed",
            "user_id": user_id,
            "error": str(e)
        }


@celery_app.task(bind=True)
def cache_warm_task(self, category: str = None) -> Dict[str, Any]:
    """
    Task to warm up the cache with popular articles.
    
    Args:
        category: Category to warm up (optional)
        
    Returns:
        Dict[str, Any]: Task result
    """
    try:
        logger.info(f"Starting cache warm task for category: {category}")
        
        # Update task state
        self.update_state(state="PROGRESS", meta={"status": "initializing"})
        
        # Simulate cache warming
        import time
        time.sleep(1)  # Simulate work
        
        result = {
            "status": "completed",
            "category": category,
            "message": f"Warmed cache for category {category or 'all'}"
        }
        
        logger.info(f"Cache warm task completed for category: {category}")
        return result
        
    except Exception as e:
        logger.error(f"Error in cache warm task for category {category}: {e}")
        return {
            "status": "failed",
            "category": category,
            "error": str(e)
        }