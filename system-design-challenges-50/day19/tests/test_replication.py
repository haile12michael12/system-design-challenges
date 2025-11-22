import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from app.services.replication_service import ReplicationService
from app.core.config import settings


class TestReplicationService:
    """Test replication service functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_replication_service(self):
        """Setup replication service with temporary directories"""
        # Create temporary directories
        self.temp_primary = tempfile.mkdtemp()
        self.temp_replica1 = tempfile.mkdtemp()
        self.temp_replica2 = tempfile.mkdtemp()
        
        # Override settings
        settings.STORAGE_PATH = self.temp_primary
        settings.REPLICA1_PATH = self.temp_replica1
        settings.REPLICA2_PATH = self.temp_replica2
        
        # Initialize replication service
        self.replication_service = ReplicationService()
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_primary, ignore_errors=True)
        shutil.rmtree(self.temp_replica1, ignore_errors=True)
        shutil.rmtree(self.temp_replica2, ignore_errors=True)
    
    def test_replication_service_initialization(self):
        """Test replication service initialization"""
        assert self.replication_service.primary_path == self.temp_primary
        assert self.replication_service.replica1_path == self.temp_replica1
        assert self.replication_service.replica2_path == self.temp_replica2
    
    def test_sync_file_to_replicas(self):
        """Test synchronizing file to replicas"""
        # Create a test file in primary storage
        file_id = "test_file_123"
        file_content = b"Hello, World!"
        primary_file_path = os.path.join(self.temp_primary, file_id)
        
        with open(primary_file_path, "wb") as f:
            f.write(file_content)
        
        # Sync file to replicas
        result = self.replication_service.sync_file_to_replicas(file_id)
        
        # Verify results
        assert result["replica1"] == True
        assert result["replica2"] == True
        
        # Verify files exist in replicas
        replica1_file_path = os.path.join(self.temp_replica1, file_id)
        replica2_file_path = os.path.join(self.temp_replica2, file_id)
        
        assert os.path.exists(replica1_file_path)
        assert os.path.exists(replica2_file_path)
        
        # Verify content matches
        with open(replica1_file_path, "rb") as f:
            assert f.read() == file_content
        
        with open(replica2_file_path, "rb") as f:
            assert f.read() == file_content
    
    def test_remove_file_from_replicas(self):
        """Test removing file from replicas"""
        # Create test files in all locations
        file_id = "test_file_456"
        file_content = b"Test content"
        
        # Create in primary
        primary_file_path = os.path.join(self.temp_primary, file_id)
        with open(primary_file_path, "wb") as f:
            f.write(file_content)
        
        # Create in replicas
        replica1_file_path = os.path.join(self.temp_replica1, file_id)
        replica2_file_path = os.path.join(self.temp_replica2, file_id)
        
        with open(replica1_file_path, "wb") as f:
            f.write(file_content)
        
        with open(replica2_file_path, "wb") as f:
            f.write(file_content)
        
        # Verify files exist
        assert os.path.exists(replica1_file_path)
        assert os.path.exists(replica2_file_path)
        
        # Remove file from replicas
        result = self.replication_service.remove_file_from_replicas(file_id)
        
        # Verify results
        assert result["replica1"] == True
        assert result["replica2"] == True
        
        # Verify files are removed
        assert not os.path.exists(replica1_file_path)
        assert not os.path.exists(replica2_file_path)
    
    def test_get_replica_status(self):
        """Test getting replica status"""
        # Initially all should be empty
        status = self.replication_service.get_replica_status()
        
        assert status["primary"]["exists"] == True
        assert status["replica1"]["exists"] == True
        assert status["replica2"]["exists"] == True
        assert status["primary"]["file_count"] == 0
        assert status["replica1"]["file_count"] == 0
        assert status["replica2"]["file_count"] == 0
        
        # Add some files to primary
        for i in range(3):
            file_path = os.path.join(self.temp_primary, f"file_{i}")
            with open(file_path, "w") as f:
                f.write(f"Content {i}")
        
        # Check status again
        status = self.replication_service.get_replica_status()
        assert status["primary"]["file_count"] == 3
        assert status["replica1"]["file_count"] == 0  # Not synced yet
        assert status["replica2"]["file_count"] == 0  # Not synced yet
    
    def test_sync_all_replicas(self):
        """Test synchronizing all replicas"""
        # Add some files to primary
        test_files = ["file_1", "file_2", "file_3"]
        for filename in test_files:
            file_path = os.path.join(self.temp_primary, filename)
            with open(file_path, "w") as f:
                f.write(f"Content of {filename}")
        
        # Sync all replicas
        result = self.replication_service.sync_all_replicas()
        
        # Verify results
        assert result["replica1"] == "synchronized"
        assert result["replica2"] == "synchronized"
        
        # Verify files exist in replicas
        for filename in test_files:
            replica1_file_path = os.path.join(self.temp_replica1, filename)
            replica2_file_path = os.path.join(self.temp_replica2, filename)
            
            assert os.path.exists(replica1_file_path)
            assert os.path.exists(replica2_file_path)