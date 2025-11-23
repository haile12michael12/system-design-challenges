from kafka import KafkaProducer
from app.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class KafkaProducerWrapper:
    def __init__(self):
        self.producer = None
        self._init_producer()

    def _init_producer(self):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.producer = None

    def send(self, topic: str, value: dict):
        """Send message to Kafka topic"""
        if not self.producer:
            logger.warning("Kafka producer not initialized")
            return None
            
        try:
            future = self.producer.send(topic, value)
            return future
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {e}")
            return None

    def flush(self):
        """Flush pending messages"""
        if self.producer:
            self.producer.flush()

# Global Kafka producer instance
kafka_producer = KafkaProducerWrapper()