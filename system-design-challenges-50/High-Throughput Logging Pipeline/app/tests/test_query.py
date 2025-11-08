import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_logs():
    """
    Test querying logs
    """
    response = client.get("/query/", params={"service": "test-service"})
    # We expect this to return 404 because the endpoint is not implemented yet
    assert response.status_code == 404

def test_query_logs_with_api_key():
    """
    Test querying logs with API key
    """
    response = client.get("/query/", params={"service": "test-service", "api_key": "test-api-key"})
    # We expect this to return 404 because the endpoint is not implemented yet
    assert response.status_code == 404

def test_query_logs_without_api_key():
    """
    Test querying logs without API key
    """
    response = client.get("/query/", params={"service": "test-service"})
    # We expect this to return 404 because the endpoint is not implemented yet
    assert response.status_code == 404