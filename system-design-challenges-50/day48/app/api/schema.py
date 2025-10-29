from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from ..config.database import get_database
from ..services.schema_service import SchemaService
from ..models.schema_evolution import ChangeStatus

router = APIRouter(prefix="/api/v1/schema", tags=["schema"])

# Pydantic models for API
class SchemaVersionResponse(BaseModel):
    id: int
    table_id: int
    version_number: int
    schema_definition: dict
    is_current: bool
    created_at: datetime
    created_by: str
    description: Optional[str]

class SchemaChangeResponse(BaseModel):
    id: int
    schema_version_id: int
    change_type: str
    status: str
    column_name: Optional[str]
    old_value: Optional[dict]
    new_value: Optional[dict]
    change_description: Optional[str]
    applied_at: Optional[datetime]
    applied_by: Optional[str]
    error_message: Optional[str]

class SchemaCreateRequest(BaseModel):
    table_id: int
    schema_definition: dict
    description: Optional[str] = None
    created_by: str = "api"

class SchemaCompareRequest(BaseModel):
    old_schema: dict
    new_schema: dict

@router.post("/versions", response_model=SchemaVersionResponse)
async def create_schema_version(
    request: SchemaCreateRequest,
    db: Session = Depends(get_database)
):
    """Create a new schema version"""
    service = SchemaService(db)
    
    schema_version = await service.create_schema_version(
        table_id=request.table_id,
        schema_definition=request.schema_definition,
        description=request.description,
        created_by=request.created_by
    )
    
    return SchemaVersionResponse(
        id=schema_version.id,
        table_id=schema_version.table_id,
        version_number=schema_version.version_number,
        schema_definition=schema_version.schema_definition,
        is_current=schema_version.is_current,
        created_at=schema_version.created_at,
        created_by=schema_version.created_by,
        description=schema_version.description
    )

@router.get("/versions/table/{table_id}/current", response_model=SchemaVersionResponse)
async def get_current_schema(
    table_id: int,
    db: Session = Depends(get_database)
):
    """Get the current schema version for a table"""
    service = SchemaService(db)
    schema_version = await service.get_current_schema(table_id)
    
    if not schema_version:
        raise HTTPException(status_code=404, detail="No schema found for table")
    
    return SchemaVersionResponse(
        id=schema_version.id,
        table_id=schema_version.table_id,
        version_number=schema_version.version_number,
        schema_definition=schema_version.schema_definition,
        is_current=schema_version.is_current,
        created_at=schema_version.created_at,
        created_by=schema_version.created_by,
        description=schema_version.description
    )

@router.get("/versions/table/{table_id}", response_model=List[SchemaVersionResponse])
async def list_schema_versions(
    table_id: int,
    limit: int = 100,
    db: Session = Depends(get_database)
):
    """List all schema versions for a table"""
    service = SchemaService(db)
    versions = await service.list_schema_versions(table_id, limit)
    
    return [
        SchemaVersionResponse(
            id=version.id,
            table_id=version.table_id,
            version_number=version.version_number,
            schema_definition=version.schema_definition,
            is_current=version.is_current,
            created_at=version.created_at,
            created_by=version.created_by,
            description=version.description
        )
        for version in versions
    ]

@router.post("/compare")
async def compare_schemas(
    request: SchemaCompareRequest,
    db: Session = Depends(get_database)
):
    """Compare two schemas and return differences"""
    service = SchemaService(db)
    changes = await service.compare_schemas(
        request.old_schema,
        request.new_schema
    )
    
    return {
        "changes": changes,
        "change_count": len(changes)
    }

@router.post("/versions/{schema_version_id}/apply")
async def apply_schema_changes(
    schema_version_id: int,
    changes: List[Dict[str, Any]],
    applied_by: str = "api",
    db: Session = Depends(get_database)
):
    """Apply schema changes"""
    service = SchemaService(db)
    
    schema_changes = await service.apply_schema_changes(
        schema_version_id=schema_version_id,
        changes=changes,
        applied_by=applied_by
    )
    
    return [
        SchemaChangeResponse(
            id=change.id,
            schema_version_id=change.schema_version_id,
            change_type=change.change_type.value,
            status=change.status.value,
            column_name=change.column_name,
            old_value=change.old_value,
            new_value=change.new_value,
            change_description=change.change_description,
            applied_at=change.applied_at,
            applied_by=change.applied_by,
            error_message=change.error_message
        )
        for change in schema_changes
    ]

@router.post("/changes/{change_id}/rollback")
async def rollback_schema_change(
    change_id: int,
    rolled_back_by: str = "api",
    db: Session = Depends(get_database)
):
    """Rollback a schema change"""
    service = SchemaService(db)
    
    success = await service.rollback_schema_change(change_id, rolled_back_by)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to rollback schema change")
    
    return {"message": "Schema change rolled back successfully"}

@router.get("/changes/version/{schema_version_id}", response_model=List[SchemaChangeResponse])
async def get_schema_changes(
    schema_version_id: int,
    db: Session = Depends(get_database)
):
    """Get schema changes for a version"""
    # This would require adding a method to the service
    # For now, return empty list
    return []
