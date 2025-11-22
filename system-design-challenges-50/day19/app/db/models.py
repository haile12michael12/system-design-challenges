from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import Optional
import uuid

Base = declarative_base()


class FileRecord(Base):
    """Model for storing file metadata"""
    __tablename__ = "file_records"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    checksum = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    description = Column(String, nullable=True)
    storage_path = Column(String, nullable=False)
    
    def __init__(self, filename: str, size: int, checksum: str, storage_path: str, 
                 description: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.filename = filename
        self.size = size
        self.checksum = checksum
        self.storage_path = storage_path
        self.description = description


class OperationType(str, PyEnum):
    """Enumeration of WAL operation types"""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class WALRecord(Base):
    """Model for Write-Ahead Log entries"""
    __tablename__ = "wal_records"
    
    id = Column(String, primary_key=True, index=True)
    operation = Column(Enum(OperationType), nullable=False)
    file_id = Column(String, ForeignKey("file_records.id"), nullable=True)
    data = Column(LargeBinary, nullable=True)  # Serialized operation data
    checksum = Column(String, nullable=False)
    segment_id = Column(String, nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, operation: OperationType, file_id: Optional[str] = None, 
                 data: Optional[bytes] = None, segment_id: str = "", position: int = 0):
        self.id = str(uuid.uuid4())
        self.operation = operation
        self.file_id = file_id
        self.data = data
        self.segment_id = segment_id
        self.position = position
        
        # Calculate checksum of the entry
        import hashlib
        entry_data = f"{operation}{file_id}{data}{segment_id}{position}".encode()
        self.checksum = hashlib.sha256(entry_data).hexdigest()