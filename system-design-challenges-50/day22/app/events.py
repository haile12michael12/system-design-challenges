from typing import Dict, Any
import asyncio
import json
from app.mq.kafka_producer import kafka_producer
from app.config import settings

class EventManager:
    """Manages application events and publishes them to Kafka"""
    
    @staticmethod
    async def publish_event(event_type: str, payload: Dict[str, Any]):
        """Publish an event to Kafka"""
        event = {
            "event_type": event_type,
            "payload": payload,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        await kafka_producer.send(
            "feed_events",
            json.dumps(event).encode('utf-8')
        )

# Global event manager instance
event_manager = EventManager()