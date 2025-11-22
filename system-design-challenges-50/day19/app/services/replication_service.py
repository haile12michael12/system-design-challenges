import os
import shutil
import time
from typing import Dict, List, Optional
from datetime import datetime
import threading

from app.core.config import settings
from app.db.models import OperationType
from app.db.repository import WALRecordRepository
from app.db.session import get_db_session
from app.services.wal_service import WALService


class ReplicationService:
    """Service for handling synchronous and asynchronous replication"""
    
    def __init__(self):
        self.primary_path = settings.STORAGE_PATH
        self.replica1_path = settings.REPLICA1_PATH
        self.replica2_path = settings.REPLICA2_PATH
        self.wal_service = WALService()
        self.replication_lock = threading.Lock()
    
    def _ensure_replica_directories(self):
        """Ensure replica directories exist"""
        os.makedirs(self.replica1_path, exist_ok=True)
        os.makedirs(self.replica2_path, exist_ok=True)
    
    def _copy_file_to_replica(self, file_path: str, replica_path: str) -> bool:
        """Copy a file to a replica directory"""
        try:
            if os.path.exists(file_path):
                replica_file_path = os.path.join(replica_path, os.path.basename(file_path))
                shutil.copy2(file_path, replica_file_path)
                return True
            return False
        except Exception as e:
            print(f"Error copying file to replica {replica_path}: {e}")
            return False
    
    def _remove_file_from_replica(self, filename: str, replica_path: str) -> bool:
        """Remove a file from a replica directory"""
        try:
            replica_file_path = os.path.join(replica_path, filename)
            if os.path.exists(replica_file_path):
                os.remove(replica_file_path)
                return True
            return False
        except Exception as e:
            print(f"Error removing file from replica {replica_path}: {e}")
            return False
    
    def sync_file_to_replicas(self, file_id: str) -> Dict[str, bool]:
        """Synchronously replicate a file to all replicas"""
        with self.replication_lock:
            self._ensure_replica_directories()
            
            # Get file path in primary storage
            primary_file_path = os.path.join(self.primary_path, file_id)
            
            # Copy to replicas
            replica1_success = self._copy_file_to_replica(primary_file_path, self.replica1_path)
            replica2_success = self._copy_file_to_replica(primary_file_path, self.replica2_path)
            
            return {
                "replica1": replica1_success,
                "replica2": replica2_success
            }
    
    def remove_file_from_replicas(self, file_id: str) -> Dict[str, bool]:
        """Remove a file from all replicas"""
        with self.replication_lock:
            self._ensure_replica_directories()
            
            # Remove from replicas
            replica1_success = self._remove_file_from_replica(file_id, self.replica1_path)
            replica2_success = self._remove_file_from_replica(file_id, self.replica2_path)
            
            return {
                "replica1": replica1_success,
                "replica2": replica2_success
            }
    
    def get_replica_status(self) -> Dict[str, dict]:
        """Get status of all replicas"""
        try:
            # Count files in each location
            primary_count = len(os.listdir(self.primary_path)) if os.path.exists(self.primary_path) else 0
            replica1_count = len(os.listdir(self.replica1_path)) if os.path.exists(self.replica1_path) else 0
            replica2_count = len(os.listdir(self.replica2_path)) if os.path.exists(self.replica2_path) else 0
            
            # Check if directories exist
            primary_exists = os.path.exists(self.primary_path)
            replica1_exists = os.path.exists(self.replica1_path)
            replica2_exists = os.path.exists(self.replica2_path)
            
            return {
                "primary": {
                    "exists": primary_exists,
                    "file_count": primary_count,
                    "path": self.primary_path
                },
                "replica1": {
                    "exists": replica1_exists,
                    "file_count": replica1_count,
                    "path": self.replica1_path
                },
                "replica2": {
                    "exists": replica2_exists,
                    "file_count": replica2_count,
                    "path": self.replica2_path
                }
            }
        except Exception as e:
            return {
                "error": f"Failed to get replica status: {e}"
            }
    
    def sync_all_replicas(self) -> Dict[str, str]:
        """Synchronize all files to replicas"""
        try:
            with self.replication_lock:
                self._ensure_replica_directories()
                
                # Clear replicas
                if os.path.exists(self.replica1_path):
                    shutil.rmtree(self.replica1_path)
                if os.path.exists(self.replica2_path):
                    shutil.rmtree(self.replica2_path)
                
                os.makedirs(self.replica1_path, exist_ok=True)
                os.makedirs(self.replica2_path, exist_ok=True)
                
                # Copy all files from primary to replicas
                if os.path.exists(self.primary_path):
                    for file in os.listdir(self.primary_path):
                        primary_file_path = os.path.join(self.primary_path, file)
                        if os.path.isfile(primary_file_path):
                            shutil.copy2(primary_file_path, os.path.join(self.replica1_path, file))
                            shutil.copy2(primary_file_path, os.path.join(self.replica2_path, file))
                
                return {
                    "replica1": "synchronized",
                    "replica2": "synchronized"
                }
        except Exception as e:
            return {
                "replica1": f"error: {e}",
                "replica2": f"error: {e}"
            }
    
    def replay_wal_operations(self, target_replica: str = "replica1") -> int:
        """Replay WAL operations on a replica"""
        try:
            # Determine target path
            if target_replica == "replica1":
                target_path = self.replica1_path
            elif target_replica == "replica2":
                target_path = self.replica2_path
            else:
                raise ValueError("Invalid replica target")
            
            # Get all WAL entries
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                entries = repo.get_latest_entries(limit=1000)  # Limit to avoid excessive operations
            
            operations_applied = 0
            
            # Apply operations in order (newest first since we're getting latest entries)
            for entry in reversed(entries):
                if entry.operation == OperationType.CREATE:
                    # Copy file from primary to replica
                    primary_file_path = os.path.join(self.primary_path, entry.file_id)
                    if os.path.exists(primary_file_path):
                        replica_file_path = os.path.join(target_path, entry.file_id)
                        shutil.copy2(primary_file_path, replica_file_path)
                        operations_applied += 1
                elif entry.operation == OperationType.DELETE:
                    # Remove file from replica
                    replica_file_path = os.path.join(target_path, entry.file_id)
                    if os.path.exists(replica_file_path):
                        os.remove(replica_file_path)
                        operations_applied += 1
            
            return operations_applied
        except Exception as e:
            print(f"Error replaying WAL operations: {e}")
            return 0