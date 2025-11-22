import os
import struct
import hashlib
from typing import List, Optional, BinaryIO
from datetime import datetime
import uuid

from app.core.config import settings
from app.core.security import calculate_checksum, verify_checksum
from app.db.models import WALRecord, OperationType
from app.db.repository import WALRecordRepository
from app.db.session import get_db_session


class WALService:
    """Write-Ahead Log manager with checksums and segment rotation"""
    
    def __init__(self):
        self.wal_path = settings.WAL_PATH
        self.segment_size = settings.WAL_SEGMENT_SIZE
        self.active_segment = None
        self.current_position = 0
        self._ensure_wal_directory()
    
    def _ensure_wal_directory(self):
        """Ensure WAL directory exists"""
        os.makedirs(self.wal_path, exist_ok=True)
        os.makedirs(os.path.join(self.wal_path, "segments"), exist_ok=True)
    
    def _get_active_segment_path(self) -> str:
        """Get path to active WAL segment"""
        return os.path.join(self.wal_path, "wal.active")
    
    def _get_segment_path(self, segment_id: str) -> str:
        """Get path to a specific WAL segment"""
        return os.path.join(self.wal_path, "segments", f"{segment_id}.wal")
    
    def _rotate_segment_if_needed(self):
        """Rotate WAL segment if current size exceeds limit"""
        if not os.path.exists(self._get_active_segment_path()):
            return
            
        if os.path.getsize(self._get_active_segment_path()) >= self.segment_size:
            # Generate new segment ID
            segment_id = str(uuid.uuid4())
            
            # Move active segment to segments directory
            segment_path = self._get_segment_path(segment_id)
            os.rename(self._get_active_segment_path(), segment_path)
            
            # Reset position counter
            self.current_position = 0
            
            # Update any pending WAL records in database with new segment ID
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                # In a real implementation, we would update the segment_id for recent entries
    
    def _write_entry_to_segment(self, entry: WALRecord) -> str:
        """Write WAL entry to active segment"""
        self._rotate_segment_if_needed()
        
        # Serialize entry data
        entry_data = f"{entry.id}|{entry.operation}|{entry.file_id}|{entry.checksum}|{entry.created_at.isoformat()}".encode()
        
        # Write to active segment
        with open(self._get_active_segment_path(), "ab") as f:
            # Write length prefix
            f.write(struct.pack("!I", len(entry_data)))
            # Write entry data
            f.write(entry_data)
            # Update position
            self.current_position += 4 + len(entry_data)
        
        return "active"  # Segment ID
    
    def log_write_operation(self, file_id: str, file_size: int) -> Optional[WALRecord]:
        """Log a file write operation"""
        try:
            # Create WAL record
            entry = WALRecord(
                operation=OperationType.CREATE,
                file_id=file_id,
                data=str(file_size).encode(),
                segment_id="",  # Will be set when written to segment
                position=self.current_position
            )
            
            # Write to database
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                db_entry = repo.create(entry)
            
            # Write to segment file
            segment_id = self._write_entry_to_segment(entry)
            
            # Update segment ID in database
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                repo.update(entry.id, segment_id=segment_id)
            
            return entry
        except Exception as e:
            print(f"Error logging write operation: {e}")
            return None
    
    def log_delete_operation(self, file_id: str) -> Optional[WALRecord]:
        """Log a file delete operation"""
        try:
            # Create WAL record
            entry = WALRecord(
                operation=OperationType.DELETE,
                file_id=file_id,
                segment_id="",  # Will be set when written to segment
                position=self.current_position
            )
            
            # Write to database
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                db_entry = repo.create(entry)
            
            # Write to segment file
            segment_id = self._write_entry_to_segment(entry)
            
            # Update segment ID in database
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                repo.update(entry.id, segment_id=segment_id)
            
            return entry
        except Exception as e:
            print(f"Error logging delete operation: {e}")
            return None
    
    def get_entries(self, limit: int = 100, offset: int = 0) -> List[WALRecord]:
        """Get WAL entries from database"""
        try:
            with get_db_session() as db:
                repo = WALRecordRepository(db)
                return repo.get_all(skip=offset, limit=limit)
        except Exception as e:
            print(f"Error retrieving WAL entries: {e}")
            return []
    
    def list_segments(self) -> List[str]:
        """List all WAL segments"""
        try:
            segments_dir = os.path.join(self.wal_path, "segments")
            if not os.path.exists(segments_dir):
                return []
            
            segments = []
            for file in os.listdir(segments_dir):
                if file.endswith(".wal"):
                    segments.append(file[:-4])  # Remove .wal extension
            return segments
        except Exception as e:
            print(f"Error listing WAL segments: {e}")
            return []
    
    def inspect_segment(self, segment_id: str) -> dict:
        """Inspect a specific WAL segment"""
        try:
            segment_path = self._get_segment_path(segment_id)
            if not os.path.exists(segment_path):
                return {"error": "Segment not found"}
            
            entries = []
            with open(segment_path, "rb") as f:
                while True:
                    # Read length prefix
                    length_bytes = f.read(4)
                    if not length_bytes:
                        break
                    
                    length = struct.unpack("!I", length_bytes)[0]
                    
                    # Read entry data
                    entry_data = f.read(length)
                    if not entry_data:
                        break
                    
                    # Parse entry data
                    try:
                        entry_str = entry_data.decode()
                        parts = entry_str.split("|")
                        if len(parts) >= 5:
                            entries.append({
                                "id": parts[0],
                                "operation": parts[1],
                                "file_id": parts[2],
                                "checksum": parts[3],
                                "timestamp": parts[4]
                            })
                    except Exception as parse_error:
                        entries.append({"raw_data": entry_data.hex(), "error": str(parse_error)})
            
            return {
                "segment_id": segment_id,
                "entries": entries,
                "size": os.path.getsize(segment_path)
            }
        except Exception as e:
            return {"error": f"Error inspecting segment: {e}"}