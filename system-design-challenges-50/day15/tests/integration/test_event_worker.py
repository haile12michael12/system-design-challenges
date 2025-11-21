import pytest
from app.workers.tasks.handle_post_created import handle_post_created_task

def test_handle_post_created_task():
    """Test the handle post created task."""
    test_message = '{"post_id": "test-123", "content": "Test content", "author": "Test Author"}'
    
    # Execute the task
    result = handle_post_created_task(test_message)
    
    # Verify the result
    assert result["status"] == "processed"
    assert result["message"] == test_message