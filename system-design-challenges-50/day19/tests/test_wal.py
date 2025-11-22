import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from app.services.wal_service import WALService
from app.db.models import OperationType
from app.core.config import settings


class TestWALService:
    """Test WAL service functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_wal_service(self):
        """Setup WAL service with temporary directory"""
        # Create temporary directory for WAL
        self.temp_dir = tempfile.mkdtemp()
        settings.WAL_PATH = self.temp_dir
        settings.WAL_SEGMENT_SIZE = 1024  # Small segment size for testing
        
        # Initialize WAL service
        self.wal_service = WALService()
        
        yield
        
        # Cleanup
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_wal_service_initialization(self):
        """Test WAL service initialization"""
        assert self.wal_service.wal_path == self.temp_dir
        assert self.wal_service.segment_size == 1024
        assert os.path.exists(self.temp_dir)
        assert os.path.exists(os.path.join(self.temp_dir, "segments"))
    
    def test_log_write_operation(self):
        """Test logging write operation"""
        file_id = "test_file_123"
        file_size = 1024
        
        # Mock database operations
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                entry = self.wal_service.log_write_operation(file_id, file_size)
                
                # Verify database operations
                mock_repo.create.assert_called_once()
                mock_repo.update.assert_called_once()
                
                # Verify entry properties
                assert entry.operation == OperationType.CREATE
                assert entry.file_id == file_id
                assert entry.data == str(file_size).encode()
    
    def test_log_delete_operation(self):
        """Test logging delete operation"""
        file_id = "test_file_456"
        
        # Mock database operations
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                entry = self.wal_service.log_delete_operation(file_id)
                
                # Verify database operations
                mock_repo.create.assert_called_once()
                mock_repo.update.assert_called_once()
                
                # Verify entry properties
                assert entry.operation == OperationType.DELETE
                assert entry.file_id == file_id
    
    def test_segment_rotation(self):
        """Test WAL segment rotation"""
        # Write enough data to trigger rotation
        file_id = "test_file"
        
        # Mock database operations
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                # Write multiple entries to trigger rotation
                for i in range(20):
                    self.wal_service.log_write_operation(f"{file_id}_{i}", 100)
                
                # Verify segments were created
                segments = self.wal_service.list_segments()
                assert len(segments) > 0
    
    def test_list_segments(self):
        """Test listing WAL segments"""
        # Initially should be empty
        segments = self.wal_service.list_segments()
        assert isinstance(segments, list)
        
        # Add a segment by writing data
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                # Write enough data to create a segment
                for i in range(10):
                    self.wal_service.log_write_operation(f"file_{i}", 100)
                
                # List segments again
                segments = self.wal_service.list_segments()
                assert isinstance(segments, list)
    
    def test_inspect_segment(self):
        """Test inspecting WAL segment"""
        # Test with non-existent segment
        result = self.wal_service.inspect_segment("non_existent")
        assert "error" in result
        
        # Test with existing segment
        with patch('app.db.session.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_repo = MagicMock()
            with patch('app.db.repository.WALRecordRepository', return_value=mock_repo):
                # Write an entry to create a segment
                self.wal_service.log_write_operation("test_file", 100)
                
                # Get segments and inspect the first one
                segments = self.wal_service.list_segments()
                if segments:
                    result = self.wal_service.inspect_segment(segments[0])
                    assert "segment_id" in result
                    assert "entries" in result