import json
import asyncio
from typing import Callable, Any

from ..core.logging_config import logger
from .schemas import EventSchema
from ..cache.redis_client import get_redis_client


class EventConsumer:
    """Consumes events from the message bus."""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler: Callable[[EventSchema], Any]) -> None:
        """
        Register a handler for a specific event type.
        
        Args:
            event_type: Type of event to handle
            handler: Function to handle the event
        """
        self.handlers[event_type] = handler
        logger.info(f"Handler registered for event type: {event_type}")
    
    async def consume_from_stream(self, stream_name: str, last_id: str = "$") -> None:
        """
        Consume events from a Redis stream.
        
        Args:
            stream_name: Name of the stream
            last_id: Last ID processed (for resuming)
        """
        try:
            while True:
                # Read events from stream
                response = self.redis_client.client.xread(
                    {stream_name: last_id}, 
                    count=1, 
                    block=1000  # Block for 1 second
                )
                
                if response:
                    stream, messages = response[0]
                    message_id, message_data = messages[0]
                    last_id = message_id
                    
                    # Process the event
                    await self._process_event(message_data.get(b"data", b"").decode("utf-8"))
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error consuming events from stream {stream_name}: {e}")
    
    async def consume_from_queue(self, queue_name: str) -> None:
        """
        Consume events from a Redis queue.
        
        Args:
            queue_name: Name of the queue
        """
        try:
            while True:
                # Read event from queue
                event_json = self.redis_client.client.brpop(queue_name, timeout=1)
                
                if event_json:
                    # Process the event
                    await self._process_event(event_json[1])
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error consuming events from queue {queue_name}: {e}")
    
    async def _process_event(self, event_json: str) -> None:
        """
        Process an event.
        
        Args:
            event_json: JSON string of the event
        """
        try:
            # Parse the event
            event_data = json.loads(event_json)
            event = EventSchema(**event_data)
            
            # Get the handler for this event type
            handler = self.handlers.get(event.event_type)
            if handler:
                # Process the event
                await handler(event)
                logger.info(f"Event {event.event_id} of type {event.event_type} processed successfully")
            else:
                logger.warning(f"No handler found for event type: {event.event_type}")
                
        except Exception as e:
            logger.error(f"Error processing event: {e}")