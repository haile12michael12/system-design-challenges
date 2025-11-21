from typing import Any, Dict
import json

class EventConsumer:
    def __init__(self):
        # In a real implementation, this would connect to a message broker
        pass
    
    def consume(self, event_type: str, handler):
        """Consume events of a specific type"""
        # In a real implementation, this would consume from a message broker
        print(f"Consuming events of type: {event_type}")
        return True

def handle_order_created(event_data: Dict[str, Any]):
    """Handle order created event"""
    print(f"Handling order created event: {event_data}")
    # Process the event
    return True

def handle_payment_processed(event_data: Dict[str, Any]):
    """Handle payment processed event"""
    print(f"Handling payment processed event: {event_data}")
    # Process the event
    return True