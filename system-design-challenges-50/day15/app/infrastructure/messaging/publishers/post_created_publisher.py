import json
from ...domain.events.post_created import PostCreated
from ..broker import message_broker

class PostCreatedPublisher:
    @staticmethod
    def publish(event: PostCreated):
        message = {
            "post_id": str(event.post_id.value),
            "content": event.content,
            "author": event.author,
            "created_at": event.created_at.isoformat() if event.created_at else None
        }
        message_broker.publish("post.created", json.dumps(message))