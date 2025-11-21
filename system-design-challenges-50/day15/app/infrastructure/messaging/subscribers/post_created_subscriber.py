import json
from ..broker import message_broker

class PostCreatedSubscriber:
    def __init__(self):
        message_broker.subscribe("post.created", self.handle_post_created)
    
    def handle_post_created(self, message: str):
        data = json.loads(message)
        print(f"Handling post created event: {data}")
        # In a real implementation, this would process the event
        # For example, update feed caches, send notifications, etc.