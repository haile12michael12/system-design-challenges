import pika
import json
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

def process_order_event(ch, method, properties, body):
    """Process order event from RabbitMQ"""
    try:
        # Parse the message
        event_data = json.loads(body)
        event_type = event_data.get("event_type")
        data = event_data.get("data", {})
        
        print(f"Processing {event_type} event: {data}")
        
        # Process based on event type
        if event_type == "order_created":
            handle_order_created(data)
        elif event_type == "order_updated":
            handle_order_updated(data)
        elif event_type == "order_cancelled":
            handle_order_cancelled(data)
        else:
            print(f"Unknown event type: {event_type}")
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing event: {e}")
        # Reject the message and requeue it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def handle_order_created(data: Dict[str, Any]):
    """Handle order created event"""
    print(f"Handling order created: {data}")
    # In a real implementation, we would:
    # 1. Update inventory
    # 2. Send notification to customer
    # 3. Trigger payment processing
    # 4. Update order status

def handle_order_updated(data: Dict[str, Any]):
    """Handle order updated event"""
    print(f"Handling order updated: {data}")
    # In a real implementation, we would:
    # 1. Send notification to customer
    # 2. Update related systems

def handle_order_cancelled(data: Dict[str, Any]):
    """Handle order cancelled event"""
    print(f"Handling order cancelled: {data}")
    # In a real implementation, we would:
    # 1. Refund payment
    # 2. Restore inventory
    # 3. Send notification to customer

def start_consumer():
    """Start consuming order events from RabbitMQ"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue='order_events', durable=True)
        
        # Set up consumer
        channel.basic_consume(queue='order_events', on_message_callback=process_order_event)
        
        print("Waiting for order events. To exit press CTRL+C")
        channel.start_consuming()
        
    except KeyboardInterrupt:
        print("Stopping consumer...")
        connection.close()
    except Exception as e:
        print(f"Error in consumer: {e}")