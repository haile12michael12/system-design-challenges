from typing import Any, Dict
import json

class EventProducer:
    def __init__(self):
        # In a real implementation, this would connect to a message broker
        pass
    
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event"""
        # In a real implementation, this would publish to a message broker
        print(f"Publishing event: {event_type} with data: {data}")
        return True

# Global event producer instance
event_producer = EventProducer()