from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging

from ..models.schema_evolution import SchemaVersion, SchemaChange, ChangeType, ChangeStatus
from ..models.data_lake import DataLakeTable
from ..config.settings import settings

logger = logging.getLogger(__name__)

class SchemaService:
    """Service for managing schema evolution"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_schema_version(
        self,
        table_id: int,
        schema_definition: Dict[str, Any],
        description: str = None,
        created_by: str = "system"
    ) -> SchemaVersion:
        """Create a new schema version for a table"""
        
        # Get current version number
        current_version = self.db.query(SchemaVersion).filter(
            SchemaVersion.table_id == table_id
        ).order_by(SchemaVersion.version_number.desc()).first()
        
        version_number = (current_version.version_number + 1) if current_version else 1
        
        # Mark previous version as not current
        if current_version:
            current_version.is_current = False
        
        # Create new schema version
        schema_version = SchemaVersion(
            table_id=table_id,
            version_number=version_number,
            schema_definition=schema_definition,
            is_current=True,
            created_by=created_by,
            description=description
        )
        
        self.db.add(schema_version)
        self.db.commit()
        self.db.refresh(schema_version)
        
        # Update table schema version
        table = self.db.query(DataLakeTable).filter(DataLakeTable.id == table_id).first()
        if table:
            table.schema_version = version_number
            self.db.commit()
        
        logger.info(f"Created schema version {version_number} for table {table_id}")
        return schema_version
    
    async def get_current_schema(self, table_id: int) -> Optional[SchemaVersion]:
        """Get the current schema version for a table"""
        return self.db.query(SchemaVersion).filter(
            SchemaVersion.table_id == table_id,
            SchemaVersion.is_current == True
        ).first()
    
    async def list_schema_versions(
        self,
        table_id: int,
        limit: int = 100
    ) -> List[SchemaVersion]:
        """List all schema versions for a table"""
        return self.db.query(SchemaVersion).filter(
            SchemaVersion.table_id == table_id
        ).order_by(SchemaVersion.version_number.desc()).limit(limit).all()
    
    async def compare_schemas(
        self,
        old_schema: Dict[str, Any],
        new_schema: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Compare two schemas and return differences"""
        changes = []
        
        old_fields = {field["name"]: field for field in old_schema.get("fields", [])}
        new_fields = {field["name"]: field for field in new_schema.get("fields", [])}
        
        # Check for added fields
        for field_name, field_def in new_fields.items():
            if field_name not in old_fields:
                changes.append({
                    "type": ChangeType.ADD_COLUMN,
                    "column_name": field_name,
                    "new_value": field_def,
                    "description": f"Added column: {field_name}"
                })
        
        # Check for removed fields
        for field_name, field_def in old_fields.items():
            if field_name not in new_fields:
                changes.append({
                    "type": ChangeType.DROP_COLUMN,
                    "column_name": field_name,
                    "old_value": field_def,
                    "description": f"Removed column: {field_name}"
                })
        
        # Check for modified fields
        for field_name in old_fields:
            if field_name in new_fields:
                old_field = old_fields[field_name]
                new_field = new_fields[field_name]
                
                if old_field != new_field:
                    changes.append({
                        "type": ChangeType.CHANGE_TYPE,
                        "column_name": field_name,
                        "old_value": old_field,
                        "new_value": new_field,
                        "description": f"Modified column: {field_name}"
                    })
        
        return changes
    
    async def apply_schema_changes(
        self,
        schema_version_id: int,
        changes: List[Dict[str, Any]],
        applied_by: str = "system"
    ) -> List[SchemaChange]:
        """Apply schema changes to the database"""
        
        schema_changes = []
        
        for change_data in changes:
            change = SchemaChange(
                schema_version_id=schema_version_id,
                change_type=change_data["type"],
                column_name=change_data.get("column_name"),
                old_value=change_data.get("old_value"),
                new_value=change_data.get("new_value"),
                change_description=change_data.get("description")
            )
            
            try:
                # Apply the change (simplified - in reality you'd execute DDL)
                await self._execute_schema_change(change)
                
                change.status = ChangeStatus.APPLIED
                change.applied_at = datetime.utcnow()
                change.applied_by = applied_by
                
            except Exception as e:
                logger.error(f"Failed to apply schema change: {str(e)}")
                change.status = ChangeStatus.FAILED
                change.error_message = str(e)
            
            self.db.add(change)
            schema_changes.append(change)
        
        self.db.commit()
        return schema_changes
    
    async def _execute_schema_change(self, change: SchemaChange):
        """Execute a schema change (simplified implementation)"""
        # In a real implementation, this would:
        # 1. Generate appropriate DDL statements
        # 2. Execute them against the database
        # 3. Update metadata tables
        # 4. Handle rollback scenarios
        
        logger.info(f"Executing schema change: {change.change_type} for column {change.column_name}")
        
        # Simulate execution
        if change.change_type == ChangeType.ADD_COLUMN:
            logger.info(f"Adding column: {change.column_name}")
        elif change.change_type == ChangeType.DROP_COLUMN:
            logger.info(f"Dropping column: {change.column_name}")
        elif change.change_type == ChangeType.CHANGE_TYPE:
            logger.info(f"Changing type for column: {change.column_name}")
    
    async def rollback_schema_change(self, change_id: int, rolled_back_by: str = "system") -> bool:
        """Rollback a schema change"""
        change = self.db.query(SchemaChange).filter(SchemaChange.id == change_id).first()
        if not change:
            return False
        
        if change.status != ChangeStatus.APPLIED:
            return False
        
        try:
            # Execute rollback (simplified)
            await self._execute_rollback(change)
            
            change.status = ChangeStatus.ROLLED_BACK
            change.rolled_back_at = datetime.utcnow()
            change.rolled_back_by = rolled_back_by
            
            self.db.commit()
            
            logger.info(f"Rolled back schema change: {change.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback schema change {change.id}: {str(e)}")
            return False
    
    async def _execute_rollback(self, change: SchemaChange):
        """Execute rollback for a schema change"""
        # In a real implementation, this would execute the reverse operation
        logger.info(f"Rolling back schema change: {change.change_type} for column {change.column_name}")
