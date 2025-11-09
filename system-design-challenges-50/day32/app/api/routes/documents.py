from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db_session
from app.db.crud import DocumentCRUD
from app.db.models import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/documents", tags=["documents"])

class DocumentCreate(BaseModel):
    title: str
    content: str
    owner_id: str

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Create a new document
    """
    db_document = await DocumentCRUD.create_document(
        db, document.title, document.content, document.owner_id
    )
    if not db_document:
        raise HTTPException(status_code=500, detail="Failed to create document")
    return db_document

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db_session)):
    """
    Get a document by ID
    """
    db_document = await DocumentCRUD.get_document(db, document_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.get("/", response_model=List[DocumentResponse])
async def get_documents_by_owner(
    owner_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get documents by owner
    """
    documents = await DocumentCRUD.get_documents_by_owner(db, owner_id, skip, limit)
    return documents

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str, 
    document_update: DocumentUpdate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a document
    """
    db_document = await DocumentCRUD.update_document(
        db, document_id, document_update.title, document_update.content
    )
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, db: AsyncSession = Depends(get_db_session)):
    """
    Delete a document
    """
    success = await DocumentCRUD.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")