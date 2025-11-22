import os
import hashlib
from typing import Optional, Dict
from pathlib import Path

from app.core.config import settings
from app.core.security import calculate_checksum


class LocalStore:
    """Local filesystem storage abstraction"""
    
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or settings.STORAGE_PATH
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure storage directory exists"""
        os.makedirs(self.base_path, exist_ok=True)
    
    def _get_file_path(self, file_id: str) -> str:
        """Get full path for a file ID"""
        return os.path.join(self.base_path, file_id)
    
    def save_file(self, file_id: str, content: bytes) -> str:
        """Save file content to storage"""
        try:
            file_path = self._get_file_path(file_id)
            
            # Write content to file
            with open(file_path, "wb") as f:
                f.write(content)
            
            return file_path
        except Exception as e:
            raise Exception(f"Failed to save file: {e}")
    
    def get_file(self, file_id: str) -> Optional[bytes]:
        """Retrieve file content from storage"""
        try:
            file_path = self._get_file_path(file_id)
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from storage"""
        try:
            file_path = self._get_file_path(file_id)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def file_exists(self, file_id: str) -> bool:
        """Check if a file exists in storage"""
        file_path = self._get_file_path(file_id)
        return os.path.exists(file_path)
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, str]]:
        """Get file metadata"""
        try:
            file_path = self._get_file_path(file_id)
            
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            
            # Read file to calculate checksum
            with open(file_path, "rb") as f:
                content = f.read()
                checksum = calculate_checksum(content)
            
            return {
                "file_id": file_id,
                "size": stat.st_size,
                "checksum": checksum,
                "created_at": str(stat.st_ctime),
                "modified_at": str(stat.st_mtime)
            }
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def list_files(self) -> list:
        """List all files in storage"""
        try:
            if not os.path.exists(self.base_path):
                return []
            
            files = []
            for file in os.listdir(self.base_path):
                file_path = os.path.join(self.base_path, file)
                if os.path.isfile(file_path):
                    files.append(file)
            
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def get_storage_usage(self) -> Dict[str, int]:
        """Get storage usage statistics"""
        try:
            total_size = 0
            file_count = 0
            
            if os.path.exists(self.base_path):
                for file in os.listdir(self.base_path):
                    file_path = os.path.join(self.base_path, file)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            return {
                "total_size": total_size,
                "file_count": file_count
            }
        except Exception as e:
            print(f"Error getting storage usage: {e}")
            return {
                "total_size": 0,
                "file_count": 0
            }