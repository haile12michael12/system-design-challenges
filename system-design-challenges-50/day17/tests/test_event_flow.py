import pytest
from unittest.mock import Mock, patch, AsyncMock
import json

from app.domain.events.post_created import PostCreatedEvent
from app.domain.events.follower_added import FollowerAddedEvent
from app.message_bus.event_publisher import EventPublisher
from app.message_bus.event_consumer import EventConsumer
from app.message_bus.schemas import PostCreatedEventSchema, FollowerAddedEventSchema


@pytest.fixture
def mock_post_created_event():
    """Create a mock post created event."""
    return PostCreatedEvent(
        post_id="test_post_id",
        user_id="test_user_id",
        content="Test post content"
    )


@pytest.fixture
def mock_follower_added_event():
    """Create a mock follower added event."""
    return FollowerAddedEvent(
        follower_id="test_follower_id",
        followed_id="test_followed_id"
    )


@pytest.mark.asyncio
async def test_publish_post_created_event(mock_post_created_event):
    """Test publishing a post created event."""
    # Arrange
    with patch('app.message_bus.event_publisher.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        mock_redis_client.client = Mock()
        mock_redis_client.client.xadd.return_value = "test_stream_id"
        
        publisher = EventPublisher()
        
        # Act
        result = await publisher.publish(mock_post_created_event)
        
        # Assert
        assert result is True
        mock_redis_client.client.xadd.assert_called_once()
        # Check that the stream name is correctly formatted
        call_args = mock_redis_client.client.xadd.call_args
        stream_name = call_args[0][0]
        assert stream_name == f"events:{mock_post_created_event.event_type}"


@pytest.mark.asyncio
async def test_publish_follower_added_event(mock_follower_added_event):
    """Test publishing a follower added event."""
    # Arrange
    with patch('app.message_bus.event_publisher.get_redis_client') as mock_redis_factory:
        mock_redis_client = Mock()
        mock_redis_factory.return_value = mock_redis_client
        mock_redis_client.client = Mock()
        mock_redis_client.client.xadd.return_value = "test_stream_id"
        
        publisher = EventPublisher()
        
        # Act
        result = await publisher.publish(mock_follower_added_event)
        
        # Assert
        assert result is True
        mock_redis_client.client.xadd.assert_called_once()
        # Check that the stream name is correctly formatted
        call_args = mock_redis_client.client.xadd.call_args
        stream_name = call_args[0][0]
        assert stream_name == f"events:{mock_follower_added_event.event_type}"


@pytest.mark.asyncio
async def test_register_event_handler():
    """Test registering an event handler."""
    # Arrange
    consumer = EventConsumer()
    mock_handler = Mock()
    
    # Act
    consumer.register_handler("test_event_type", mock_handler)
    
    # Assert
    assert "test_event_type" in consumer.handlers
    assert consumer.handlers["test_event_type"] == mock_handler


@pytest.mark.asyncio
async def test_process_post_created_event(mock_post_created_event):
    """Test processing a post created event."""
    # Arrange
    consumer = EventConsumer()
    mock_handler = AsyncMock()
    consumer.register_handler("post_created", mock_handler)
    
    # Convert event to JSON as it would be received from Redis
    event_json = json.dumps(mock_post_created_event.dict())
    
    # Act
    await consumer._process_event(event_json)
    
    # Assert
    mock_handler.assert_called_once()
    # Check that the handler was called with the correct event
    call_args = mock_handler.call_args
    event_arg = call_args[0][0]
    assert isinstance(event_arg, PostCreatedEventSchema)
    assert event_arg.post_id == mock_post_created_event.post_id
    assert event_arg.user_id == mock_post_created_event.user_id


if __name__ == "__main__":
    pytest.main([__file__])