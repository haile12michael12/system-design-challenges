from ..celery_app import celery_app
from ...infrastructure.messaging.subscribers.post_created_subscriber import PostCreatedSubscriber

@celery_app.task
def handle_post_created_task(message: str):
    """Handle post created event in a background task."""
    subscriber = PostCreatedSubscriber()
    subscriber.handle_post_created(message)
    return {"status": "processed", "message": message}