from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc, update
from typing import List, Optional, Sequence, cast
from app.db.models import Document, DocumentVersion, DocumentOperation
from app.core.logger import get_logger
import uuid
from datetime import datetime

logger = get_logger("db.crud")

class DocumentCRUD:
    @staticmethod
    async def get_document(db: AsyncSession, document_id: str) -> Optional[Document]:
        """
        Get a document by ID
        """
        try:
            result = await db.execute(select(Document).where(Document.id == document_id))
            document = result.scalar_one_or_none()
            return document
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {str(e)}")
            return None
            
    @staticmethod
    async def get_documents_by_owner(db: AsyncSession, owner_id: str, skip: int = 0, limit: int = 100) -> List[Document]:
        """
        Get documents by owner
        """
        try:
            result = await db.execute(
                select(Document)
                .where(Document.owner_id == owner_id)
                .offset(skip)
                .limit(limit)
                .order_by(desc(Document.created_at))
            )
            documents = list(result.scalars().all())
            return documents
        except Exception as e:
            logger.error(f"Failed to get documents for owner {owner_id}: {str(e)}")
            return []
            
    @staticmethod
    async def create_document(db: AsyncSession, title: str, content: str, owner_id: str) -> Optional[Document]:
        """
        Create a new document
        """
        try:
            document = Document(
                title=title,
                content=content,
                owner_id=owner_id
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)
            logger.info(f"Created document {document.id}")
            return document
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create document: {str(e)}")
            return None
            
    @staticmethod
    async def update_document(db: AsyncSession, document_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Document]:
        """
        Update a document
        """
        try:
            document = await DocumentCRUD.get_document(db, document_id)
            if not document:
                return None
                
            # Update fields if provided
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if content is not None:
                update_data['content'] = content
                
            if update_data:
                stmt = update(Document).where(Document.id == document_id).values(**update_data)
                await db.execute(stmt)
                await db.commit()
                await db.refresh(document)
                logger.info(f"Updated document {document_id}")
            return document
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update document {document_id}: {str(e)}")
            return None
            
    @staticmethod
    async def delete_document(db: AsyncSession, document_id: str) -> bool:
        """
        Delete a document
        """
        try:
            document = await DocumentCRUD.get_document(db, document_id)
            if not document:
                return False
                
            await db.delete(document)
            await db.commit()
            logger.info(f"Deleted document {document_id}")
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to delete document {document_id}: {str(e)}")
            return False
            
    @staticmethod
    async def create_document_version(db: AsyncSession, document_id: str, content: str, created_by: str) -> Optional[DocumentVersion]:
        """
        Create a document version
        """
        try:
            # Get the latest version number
            result = await db.execute(
                select(DocumentVersion.version_number)
                .where(DocumentVersion.document_id == document_id)
                .order_by(desc(DocumentVersion.version_number))
                .limit(1)
            )
            latest_version = result.scalar_one_or_none()
            version_number = (latest_version or 0) + 1
            
            version = DocumentVersion(
                document_id=document_id,
                content=content,
                version_number=version_number,
                created_by=created_by
            )
            db.add(version)
            await db.commit()
            await db.refresh(version)
            logger.info(f"Created document version {version.id} (v{version_number})")
            return version
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create document version: {str(e)}")
            return None
            
    @staticmethod
    async def add_document_operation(db: AsyncSession, document_id: str, operation_data: dict, user_id: str) -> Optional[DocumentOperation]:
        """
        Add a document operation
        """
        try:
            operation = DocumentOperation(
                document_id=document_id,
                operation_data=operation_data,
                user_id=user_id
            )
            db.add(operation)
            await db.commit()
            await db.refresh(operation)
            logger.info(f"Added document operation {operation.id}")
            return operation
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to add document operation: {str(e)}")
            return None