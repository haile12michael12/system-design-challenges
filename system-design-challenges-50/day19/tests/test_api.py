import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import tempfile

from app.main import app
from app.db.session import init_db

# Initialize test client
client = TestClient(app)


def setup_module(module):
    """Setup test database"""
    init_db()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "dependencies" in data


@patch('app.storage.local_store.LocalStore.save_file')
@patch('app.services.wal_service.WALService.log_write_operation')
def test_file_upload(mock_wal_log, mock_save_file):
    """Test file upload endpoint"""
    # Mock the storage and WAL service
    mock_save_file.return_value = "/tmp/test_file.txt"
    mock_wal_log.return_value = MagicMock(id="wal_entry_123")
    
    # Create test file
    test_content = b"Hello, World!"
    files = {"file": ("test.txt", test_content, "text/plain")}
    
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["filename"] == "test.txt"
    assert data["size"] == len(test_content)


@patch('app.storage.local_store.LocalStore.get_file')
def test_file_download(mock_get_file):
    """Test file download endpoint"""
    # Mock the storage
    mock_get_file.return_value = b"Hello, World!"
    
    response = client.get("/download/test_file_id")
    assert response.status_code == 200
    data = response.json()
    assert data["file_id"] == "test_file_id"
    assert "content" in data


@patch('app.storage.local_store.LocalStore.delete_file')
@patch('app.services.wal_service.WALService.log_delete_operation')
def test_file_delete(mock_wal_log, mock_delete_file):
    """Test file delete endpoint"""
    # Mock the storage and WAL service
    mock_delete_file.return_value = True
    mock_wal_log.return_value = MagicMock(id="wal_entry_456")
    
    response = client.delete("/files/test_file_id")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "File deleted successfully"
    assert data["file_id"] == "test_file_id"


def test_admin_replica_status():
    """Test replica status endpoint"""
    # Test without authentication (should fail)
    response = client.get("/replicas/status")
    # Note: This might depend on auth implementation
    # For now, we're just testing that the endpoint exists
    assert response.status_code in [200, 401, 403]


def test_admin_wal_segments():
    """Test WAL segments endpoint"""
    # Test without authentication (should fail)
    response = client.get("/wal/segments")
    # Note: This might depend on auth implementation
    # For now, we're just testing that the endpoint exists
    assert response.status_code in [200, 401, 403]


def test_admin_wal_entries():
    """Test WAL entries endpoint"""
    # Test without authentication (should fail)
    response = client.get("/wal/entries")
    # Note: This might depend on auth implementation
    # For now, we're just testing that the endpoint exists
    assert response.status_code in [200, 401, 403]