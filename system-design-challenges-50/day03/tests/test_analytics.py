import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_track_view():
    """Test tracking a view for a question"""
    # First create a question
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    created_question = response.json()
    
    # Track a view
    response = client.post(f"/analytics/track-view/{created_question['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "View tracked successfully"

def test_get_analytics():
    """Test retrieving analytics for a question"""
    # First create a question
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    created_question = response.json()
    
    # Track a view
    response = client.post(f"/analytics/track-view/{created_question['id']}")
    assert response.status_code == 200
    
    # Retrieve analytics
    response = client.get(f"/analytics/{created_question['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["question_id"] == created_question["id"]
    assert data["views"] >= 1

def test_get_all_analytics():
    """Test retrieving analytics for all questions"""
    response = client.get("/analytics/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)