import os
import shutil
from typing import List, Dict
from datetime import datetime

from app.core.config import settings
from app.db.models import OperationType
from app.db.repository import WALRecordRepository
from app.db.session import get_db_session
from app.services.wal_service import WALService
from app.services.replication_service import ReplicationService


class RecoveryService:
    """Service for WAL replay and bootstrap on startup"""
    
    def __init__(self):
        self.wal_service = WALService()
        self.replication_service = ReplicationService()
    
    def bootstrap_system(self) -> Dict[str, str]:
        """Bootstrap the system on startup"""
        try:
            # Ensure all directories exist
            os.makedirs(settings.STORAGE_PATH, exist_ok=True)
            os.makedirs(settings.REPLICA1_PATH, exist_ok=True)
            os.makedirs(settings.REPLICA2_PATH, exist_ok=True)
            os.makedirs(settings.WAL_PATH, exist_ok=True)
            os.makedirs(os.path.join(settings.WAL_PATH, "segments"), exist_ok=True)
            
            # Replay WAL to recover state
            replay_result = self.replay_wal()
            
            # Sync replicas
            sync_result = self.replication_service.sync_all_replicas()
            
            return {
                "status": "bootstrapped",
                "wal_replay": replay_result,
                "replica_sync": sync_result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def replay_wal(self) -> Dict[str, int]:
        """Replay WAL operations to recover system state"""
        try:
            # Get all WAL entries ordered by creation time
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                entries = repo.get_latest_entries(limit=10000)  # Get a large number of entries
            
            # Process entries in chronological order (oldest first)
            create_operations = 0
            delete_operations = 0
            update_operations = 0
            
            for entry in reversed(entries):  # Reversed because get_latest_entries returns newest first
                if entry.operation == OperationType.CREATE:
                    # For CREATE operations, we would restore the file from backup or regenerate it
                    # In this simplified implementation, we just count the operation
                    create_operations += 1
                elif entry.operation == OperationType.DELETE:
                    # For DELETE operations, ensure file is removed from all locations
                    primary_file_path = os.path.join(settings.STORAGE_PATH, entry.file_id)
                    replica1_file_path = os.path.join(settings.REPLICA1_PATH, entry.file_id)
                    replica2_file_path = os.path.join(settings.REPLICA2_PATH, entry.file_id)
                    
                    # Remove from all locations
                    for file_path in [primary_file_path, replica1_file_path, replica2_file_path]:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    
                    delete_operations += 1
                elif entry.operation == OperationType.UPDATE:
                    # For UPDATE operations, we would apply the changes
                    # In this simplified implementation, we just count the operation
                    update_operations += 1
            
            return {
                "create_operations": create_operations,
                "delete_operations": delete_operations,
                "update_operations": update_operations,
                "total_operations": create_operations + delete_operations + update_operations
            }
        except Exception as e:
            return {
                "error": f"Failed to replay WAL: {e}"
            }
    
    def recover_from_replica(self, replica_name: str = "replica1") -> Dict[str, str]:
        """Recover primary storage from a replica"""
        try:
            # Determine source path
            if replica_name == "replica1":
                source_path = settings.REPLICA1_PATH
            elif replica_name == "replica2":
                source_path = settings.REPLICA2_PATH
            else:
                raise ValueError("Invalid replica name")
            
            # Clear primary storage
            if os.path.exists(settings.STORAGE_PATH):
                shutil.rmtree(settings.STORAGE_PATH)
            
            # Copy from replica to primary
            if os.path.exists(source_path):
                shutil.copytree(source_path, settings.STORAGE_PATH)
            else:
                # If replica doesn't exist, create empty directory
                os.makedirs(settings.STORAGE_PATH, exist_ok=True)
            
            return {
                "status": "recovered",
                "source": replica_name,
                "destination": "primary"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def validate_consistency(self) -> Dict[str, dict]:
        """Validate consistency between primary and replicas"""
        try:
            # Get file lists
            primary_files = set(os.listdir(settings.STORAGE_PATH)) if os.path.exists(settings.STORAGE_PATH) else set()
            replica1_files = set(os.listdir(settings.REPLICA1_PATH)) if os.path.exists(settings.REPLICA1_PATH) else set()
            replica2_files = set(os.listdir(settings.REPLICA2_PATH)) if os.path.exists(settings.REPLICA2_PATH) else set()
            
            # Check consistency
            replica1_consistent = primary_files == replica1_files
            replica2_consistent = primary_files == replica2_files
            
            return {
                "primary": {
                    "file_count": len(primary_files)
                },
                "replica1": {
                    "file_count": len(replica1_files),
                    "consistent_with_primary": replica1_consistent
                },
                "replica2": {
                    "file_count": len(replica2_files),
                    "consistent_with_primary": replica2_consistent
                },
                "overall_consistent": replica1_consistent and replica2_consistent
            }
        except Exception as e:
            return {
                "error": f"Failed to validate consistency: {e}"
            }
    
    def rebuild_wal_from_storage(self) -> Dict[str, int]:
        """Rebuild WAL entries from existing storage files"""
        try:
            created_entries = 0
            
            # Scan primary storage and create WAL entries for existing files
            if os.path.exists(settings.STORAGE_PATH):
                for filename in os.listdir(settings.STORAGE_PATH):
                    file_path = os.path.join(settings.STORAGE_PATH, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        
                        # Log as CREATE operation
                        wal_entry = self.wal_service.log_write_operation(filename, file_size)
                        if wal_entry:
                            created_entries += 1
            
            return {
                "entries_created": created_entries
            }
        except Exception as e:
            return {
                "error": f"Failed to rebuild WAL: {e}"
            }