from kafka import KafkaConsumer
from app.config import settings
import json
import logging
import threading
from typing import Callable

logger = logging.getLogger(__name__)

class KafkaConsumerWrapper:
    def __init__(self):
        self.consumer = None
        self.running = False
        self.consumer_thread = None

    def _init_consumer(self, topics: list, group_id: str):
        """Initialize Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=settings.kafka_bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True,
                auto_commit_interval_ms=1000
            )
            logger.info(f"Kafka consumer initialized for topics: {topics}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            self.consumer = None

    def start_consuming(self, topics: list, group_id: str, message_handler: Callable):
        """Start consuming messages in a separate thread"""
        if self.running:
            logger.warning("Consumer is already running")
            return

        self._init_consumer(topics, group_id)
        if not self.consumer:
            return

        self.running = True
        self.consumer_thread = threading.Thread(
            target=self._consume_messages,
            args=(message_handler,),
            daemon=True
        )
        self.consumer_thread.start()

    def _consume_messages(self, message_handler: Callable):
        """Consume messages from Kafka"""
        try:
            for message in self.consumer:
                if not self.running:
                    break
                try:
                    message_handler(message)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"Error in consumer loop: {e}")
        finally:
            self.running = False

    def stop_consuming(self):
        """Stop consuming messages"""
        self.running = False
        if self.consumer:
            self.consumer.close()

# Global Kafka consumer instance
kafka_consumer = KafkaConsumerWrapper()