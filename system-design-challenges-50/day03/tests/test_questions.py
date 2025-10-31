import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Question

client = TestClient(app)

def test_create_question():
    """Test creating a new question"""
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == question_data["title"]
    assert data["content"] == question_data["content"]
    assert "id" in data

def test_get_questions():
    """Test retrieving questions"""
    response = client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_question():
    """Test retrieving a specific question"""
    # First create a question
    question_data = {
        "title": "Test Question",
        "content": "This is a test question content"
    }
    
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    created_question = response.json()
    
    # Then retrieve it
    response = client.get(f"/questions/{created_question['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_question["id"]
    assert data["title"] == question_data["title"]