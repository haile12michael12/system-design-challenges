from app.ws.connection_manager import manager
from app.mq.kafka_consumer import kafka_consumer
from app.mq.topics import WEBSOCKET_EVENTS_TOPIC
import json
import logging

logger = logging.getLogger(__name__)

def handle_websocket_event(message):
    """Handle incoming WebSocket events from Kafka"""
    try:
        # Parse the message
        event_data = message.value
        
        # Extract event type and payload
        event_type = event_data.get("event_type")
        payload = event_data.get("payload", {})
        user_id = payload.get("user_id")
        
        # Handle different event types
        if event_type == "new_post":
            # Send notification about new post to followers
            notification = {
                "type": "new_post",
                "data": payload
            }
            if user_id:
                # Send to specific user
                manager.send_personal_message(notification, user_id)
            else:
                # Broadcast to all users
                manager.broadcast(notification)
                
        elif event_type == "new_follower":
            # Send notification about new follower
            notification = {
                "type": "new_follower",
                "data": payload
            }
            if user_id:
                manager.send_personal_message(notification, user_id)
                
        elif event_type == "like":
            # Send notification about post like
            notification = {
                "type": "like",
                "data": payload
            }
            if user_id:
                manager.send_personal_message(notification, user_id)
                
        logger.info(f"Handled WebSocket event: {event_type}")
        
    except Exception as e:
        logger.error(f"Error handling WebSocket event: {e}")

def start_websocket_event_listener():
    """Start listening for WebSocket events from Kafka"""
    kafka_consumer.start_consuming(
        topics=[WEBSOCKET_EVENTS_TOPIC],
        group_id="websocket_events_group",
        message_handler=handle_websocket_event
    )
    logger.info("Started WebSocket event listener")

def stop_websocket_event_listener():
    """Stop listening for WebSocket events"""
    kafka_consumer.stop_consuming()
    logger.info("Stopped WebSocket event listener")