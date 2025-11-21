import json
from typing import Any, Callable
from ...config import settings

class MessageBroker:
    def __init__(self):
        # In a real implementation, this would connect to a message broker like RabbitMQ or Kafka
        self.subscribers = {}
    
    def publish(self, topic: str, message: Any):
        # In a real implementation, this would publish to a message broker
        print(f"Publishing to {topic}: {message}")
        # Notify subscribers if any
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)
    
    def subscribe(self, topic: str, callback: Callable):
        # In a real implementation, this would subscribe to a message broker
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

message_broker = MessageBroker()