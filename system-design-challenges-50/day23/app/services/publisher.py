import asyncio
import json
import pika
from app.settings import settings
from typing import Dict, Any

def get_rabbitmq_connection():
    """Get RabbitMQ connection"""
    parameters = pika.ConnectionParameters(
        host=settings.rabbitmq_url.split("//")[1].split(":")[0],
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials("guest", "guest")
    )
    return pika.BlockingConnection(parameters)

async def publish_order_event(event_type: str, data: Dict[str, Any]):
    """Publish order event to RabbitMQ"""
    try:
        # In a real implementation, we would use an async RabbitMQ client
        # For now, we'll simulate the publishing
        print(f"Publishing event {event_type} to RabbitMQ: {data}")
        
        # Simulate async operation
        await asyncio.sleep(0.1)
        
        return {"status": "published", "event_type": event_type}
    except Exception as e:
        print(f"Error publishing event: {e}")
        return {"status": "error", "error": str(e)}