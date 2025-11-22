from sqlalchemy.orm import Session
from typing import List, Optional, TypeVar, Generic
from app.db.models import FileRecord, WALRecord, OperationType

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model
    
    def create(self, obj: T) -> T:
        """Create a new record"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get(self, id: str) -> Optional[T]:
        """Get a record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: str, **kwargs) -> Optional[T]:
        """Update a record"""
        obj = self.get(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    def delete(self, id: str) -> bool:
        """Delete a record"""
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False


class FileRecordRepository(BaseRepository[FileRecord]):
    """Repository for FileRecord model"""
    
    def __init__(self, db: Session):
        super().__init__(db, FileRecord)
    
    def get_by_filename(self, filename: str) -> Optional[FileRecord]:
        """Get file record by filename"""
        return self.db.query(FileRecord).filter(FileRecord.filename == filename).first()
    
    def get_by_checksum(self, checksum: str) -> Optional[FileRecord]:
        """Get file record by checksum"""
        return self.db.query(FileRecord).filter(FileRecord.checksum == checksum).first()


class WALRecordRepository(BaseRepository[WALRecord]):
    """Repository for WALRecord model"""
    
    def __init__(self, db: Session):
        super().__init__(db, WALRecord)
    
    def get_by_operation(self, operation: OperationType) -> List[WALRecord]:
        """Get WAL records by operation type"""
        return self.db.query(WALRecord).filter(WALRecord.operation == operation).all()
    
    def get_by_file_id(self, file_id: str) -> List[WALRecord]:
        """Get WAL records by file ID"""
        return self.db.query(WALRecord).filter(WALRecord.file_id == file_id).all()
    
    def get_by_segment(self, segment_id: str) -> List[WALRecord]:
        """Get WAL records by segment ID"""
        return self.db.query(WALRecord).filter(WALRecord.segment_id == segment_id).all()
    
    def get_latest_entries(self, limit: int = 100) -> List[WALRecord]:
        """Get latest WAL entries"""
        return self.db.query(WALRecord).order_by(WALRecord.created_at.desc()).limit(limit).all()