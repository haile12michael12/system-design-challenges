import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from app.services.recovery_service import RecoveryService
from app.core.config import settings


class TestRecoveryService:
    """Test recovery service functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_recovery_service(self):
        """Setup recovery service with temporary directories"""
        # Create temporary directories
        self.temp_primary = tempfile.mkdtemp()
        self.temp_replica1 = tempfile.mkdtemp()
        self.temp_replica2 = tempfile.mkdtemp()
        self.temp_wal = tempfile.mkdtemp()
        
        # Override settings
        settings.STORAGE_PATH = self.temp_primary
        settings.REPLICA1_PATH = self.temp_replica1
        settings.REPLICA2_PATH = self.temp_replica2
        settings.WAL_PATH = self.temp_wal
        
        # Initialize recovery service
        self.recovery_service = RecoveryService()
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_primary, ignore_errors=True)
        shutil.rmtree(self.temp_replica1, ignore_errors=True)
        shutil.rmtree(self.temp_replica2, ignore_errors=True)
        shutil.rmtree(self.temp_wal, ignore_errors=True)
    
    def test_recovery_service_initialization(self):
        """Test recovery service initialization"""
        assert self.recovery_service.wal_service is not None
        assert self.recovery_service.replication_service is not None
    
    def test_bootstrap_system(self):
        """Test system bootstrap"""
        # Bootstrap the system
        result = self.recovery_service.bootstrap_system()
        
        # Verify directories were created
        assert os.path.exists(self.temp_primary)
        assert os.path.exists(self.temp_replica1)
        assert os.path.exists(self.temp_replica2)
        assert os.path.exists(self.temp_wal)
        assert os.path.exists(os.path.join(self.temp_wal, "segments"))
        
        # Verify result
        assert result["status"] == "bootstrapped"
        assert "wal_replay" in result
        assert "replica_sync" in result
    
    def test_replay_wal(self):
        """Test WAL replay"""
        # Mock WAL entries
        mock_entries = []
        
        # Test replay with empty WAL
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            mock_repo.get_latest_entries.return_value = mock_entries
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                result = self.recovery_service.replay_wal()
                
                # Verify result
                assert result["create_operations"] == 0
                assert result["delete_operations"] == 0
                assert result["update_operations"] == 0
                assert result["total_operations"] == 0
    
    def test_recover_from_replica(self):
        """Test recovering from replica"""
        # Create test files in replica1
        test_files = ["file_1", "file_2", "file_3"]
        for filename in test_files:
            file_path = os.path.join(self.temp_replica1, filename)
            with open(file_path, "w") as f:
                f.write(f"Content of {filename}")
        
        # Recover from replica1
        result = self.recovery_service.recover_from_replica("replica1")
        
        # Verify result
        assert result["status"] == "recovered"
        assert result["source"] == "replica1"
        assert result["destination"] == "primary"
        
        # Verify files were copied to primary
        for filename in test_files:
            primary_file_path = os.path.join(self.temp_primary, filename)
            assert os.path.exists(primary_file_path)
            
            with open(primary_file_path, "r") as f:
                assert f.read() == f"Content of {filename}"
    
    def test_validate_consistency(self):
        """Test consistency validation"""
        # Initially all should be empty and consistent
        result = self.recovery_service.validate_consistency()
        
        assert result["overall_consistent"] == True
        assert result["primary"]["file_count"] == 0
        assert result["replica1"]["file_count"] == 0
        assert result["replica2"]["file_count"] == 0
        
        # Add files to primary
        test_files = ["file_a", "file_b"]
        for filename in test_files:
            file_path = os.path.join(self.temp_primary, filename)
            with open(file_path, "w") as f:
                f.write(f"Content of {filename}")
        
        # Now replicas should be inconsistent
        result = self.recovery_service.validate_consistency()
        
        assert result["overall_consistent"] == False
        assert result["primary"]["file_count"] == 2
        assert result["replica1"]["file_count"] == 0
        assert result["replica2"]["file_count"] == 0
        assert result["replica1"]["consistent_with_primary"] == False
        assert result["replica2"]["consistent_with_primary"] == False
    
    def test_rebuild_wal_from_storage(self):
        """Test rebuilding WAL from storage"""
        # Add files to primary storage
        test_files = ["doc_1.txt", "doc_2.txt"]
        for filename in test_files:
            file_path = os.path.join(self.temp_primary, filename)
            with open(file_path, "w") as f:
                f.write(f"Content of {filename}")
        
        # Mock WAL service
        with patch('app.services.wal_service.WALService.log_write_operation') as mock_log_write:
            mock_log_write.return_value = MagicMock()
            
            # Rebuild WAL from storage
            result = self.recovery_service.rebuild_wal_from_storage()
            
            # Verify result
            assert result["entries_created"] == 2
            assert mock_log_write.call_count == 2