import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data


def test_docs_endpoint():
    """Test that the docs endpoint is available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint():
    """Test that the OpenAPI endpoint is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_get_articles_default():
    """Test getting articles with default parameters."""
    response = client.get("/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_articles_with_category():
    """Test getting articles filtered by category."""
    response = client.get("/v1/articles/?category=technology")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_articles_with_limit():
    """Test getting articles with limit parameter."""
    response = client.get("/v1/articles/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_article_by_id():
    """Test getting a specific article by ID."""
    response = client.get("/v1/articles/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)