import json
import asyncio
from typing import Any

from ..core.logging_config import logger
from .schemas import EventSchema
from ..cache.redis_client import get_redis_client


class EventPublisher:
    """Publishes events to the message bus."""
    
    def __init__(self):
        self.redis_client = get_redis_client()
    
    async def publish(self, event: EventSchema) -> bool:
        """
        Publish an event to the message bus.
        
        Args:
            event: Event to publish
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert event to JSON
            event_json = json.dumps(event.dict())
            
            # Publish to Redis stream
            stream_name = f"events:{event.event_type}"
            self.redis_client.client.xadd(stream_name, {"data": event_json})
            
            logger.info(f"Event {event.event_id} of type {event.event_type} published successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing event {event.event_id}: {e}")
            return False
    
    async def publish_to_queue(self, event: EventSchema, queue_name: str = "events") -> bool:
        """
        Publish an event to a Redis queue.
        
        Args:
            event: Event to publish
            queue_name: Name of the queue
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert event to JSON
            event_json = json.dumps(event.dict())
            
            # Publish to Redis queue
            self.redis_client.client.lpush(queue_name, event_json)
            
            logger.info(f"Event {event.event_id} published to queue {queue_name} successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing event {event.event_id} to queue {queue_name}: {e}")
            return False