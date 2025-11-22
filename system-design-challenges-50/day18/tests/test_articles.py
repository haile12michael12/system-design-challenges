import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

from app.main import app

client = TestClient(app)


@patch('app.services.news_service.NewsService.get_articles')
def test_get_articles(mock_get_articles):
    """Test getting articles."""
    # Mock the service response
    mock_articles = [
        {
            "id": 1,
            "title": "Test Article 1",
            "content": "Test content 1",
            "category": "technology",
            "author": "Test Author",
            "published_at": "2023-01-01T12:00:00Z",
            "views": 100
        }
    ]
    mock_get_articles.return_value = mock_articles
    
    response = client.get("/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Article 1"


@patch('app.services.news_service.NewsService.get_article')
def test_get_article(mock_get_article):
    """Test getting a specific article."""
    # Mock the service response
    mock_article = {
        "id": 1,
        "title": "Test Article 1",
        "content": "Test content 1",
        "category": "technology",
        "author": "Test Author",
        "published_at": "2023-01-01T12:00:00Z",
        "views": 100
    }
    mock_get_article.return_value = mock_article
    
    response = client.get("/v1/articles/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Article 1"
    assert data["id"] == 1


@patch('app.services.prefetch_service.PrefetchService.get_prefetched_articles')
def test_get_articles_with_prefetch(mock_get_prefetched_articles):
    """Test getting articles with prefetch enabled."""
    # Mock the service response
    mock_articles = [
        {
            "id": 1,
            "title": "Prefetched Article 1",
            "content": "Prefetched content 1",
            "category": "technology",
            "author": "Test Author",
            "published_at": "2023-01-01T12:00:00Z",
            "views": 150
        }
    ]
    mock_get_prefetched_articles.return_value = mock_articles
    
    response = client.get("/v1/articles/?prefetch=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Prefetched Article 1"