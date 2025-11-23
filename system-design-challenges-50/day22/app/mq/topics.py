"""Kafka topic definitions"""

# Feed-related events
FEED_EVENTS_TOPIC = "feed_events"
POST_CREATED_TOPIC = "post_created"
POST_LIKED_TOPIC = "post_liked"
POST_COMMENTED_TOPIC = "post_commented"

# User-related events
USER_REGISTERED_TOPIC = "user_registered"
USER_FOLLOWED_TOPIC = "user_followed"
USER_UNFOLLOWED_TOPIC = "user_unfollowed"

# System events
SYSTEM_METRICS_TOPIC = "system_metrics"
COST_OPTIMIZATION_TOPIC = "cost_optimization"

# Email notifications
EMAIL_NOTIFICATIONS_TOPIC = "email_notifications"

# Rollup events
ROLLUP_EVENTS_TOPIC = "rollup_events"

# WebSocket events
WEBSOCKET_EVENTS_TOPIC = "websocket_events"

# All topics
ALL_TOPICS = [
    FEED_EVENTS_TOPIC,
    POST_CREATED_TOPIC,
    POST_LIKED_TOPIC,
    POST_COMMENTED_TOPIC,
    USER_REGISTERED_TOPIC,
    USER_FOLLOWED_TOPIC,
    USER_UNFOLLOWED_TOPIC,
    SYSTEM_METRICS_TOPIC,
    COST_OPTIMIZATION_TOPIC,
    EMAIL_NOTIFICATIONS_TOPIC,
    ROLLUP_EVENTS_TOPIC,
    WEBSOCKET_EVENTS_TOPIC
]