import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_feedback():
    """Test submitting feedback for a question"""
    # First create a question
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    created_question = response.json()
    
    # Then submit feedback
    feedback_data = {
        "question_id": created_question["id"],
        "rating": 5,
        "comment": "Great question!"
    }
    
    response = client.post("/feedback/", json=feedback_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Feedback submitted successfully"

def test_get_feedback():
    """Test retrieving feedback for a question"""
    # First create a question
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    created_question = response.json()
    
    # Submit feedback
    feedback_data = {
        "question_id": created_question["id"],
        "rating": 4,
        "comment": "Good question"
    }
    
    response = client.post("/feedback/", json=feedback_data)
    assert response.status_code == 200
    
    # Retrieve feedback
    response = client.get(f"/feedback/{created_question['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0