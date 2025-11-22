from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from typing import Optional, List
import uuid
import os

from app.api.deps import get_current_user
from app.services.wal_service import WALService
from app.storage.local_store import LocalStore

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """Upload a file"""
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Read file content
        content = await file.read()
        
        # Store file
        local_store = LocalStore()
        file_path = local_store.save_file(file_id, content)
        
        # Log to WAL
        wal_service = WALService()
        wal_entry = wal_service.log_write_operation(file_id, len(content))
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "path": file_path,
            "wal_entry_id": wal_entry.id if wal_entry else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/download/{file_id}")
async def download_file(file_id: str, current_user: dict = Depends(get_current_user)):
    """Download a file by ID"""
    try:
        local_store = LocalStore()
        content = local_store.get_file(file_id)
        
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
            
        return {
            "file_id": file_id,
            "content": content.decode('utf-8')  # For text files
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download file: {str(e)}"
        )


@router.delete("/files/{file_id}")
async def delete_file(file_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a file by ID"""
    try:
        local_store = LocalStore()
        success = local_store.delete_file(file_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
            
        # Log to WAL
        wal_service = WALService()
        wal_entry = wal_service.log_delete_operation(file_id)
        
        return {
            "message": "File deleted successfully",
            "file_id": file_id,
            "wal_entry_id": wal_entry.id if wal_entry else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        )