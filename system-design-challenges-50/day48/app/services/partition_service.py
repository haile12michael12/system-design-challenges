from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, date
import logging

from ..models.data_lake import DataLakeTable, DataLakePartition
from ..config.settings import settings

logger = logging.getLogger(__name__)

class PartitionService:
    """Service for managing data lake partitions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_partition(
        self,
        table_id: int,
        partition_values: Dict[str, Any],
        record_count: int = 0,
        size_bytes: int = 0,
        file_count: int = 0
    ) -> DataLakePartition:
        """Create a new partition"""
        
        # Generate partition path
        partition_path = self._generate_partition_path(partition_values)
        
        # Check if partition already exists
        existing = self.db.query(DataLakePartition).filter(
            DataLakePartition.table_id == table_id,
            DataLakePartition.partition_path == partition_path
        ).first()
        
        if existing:
            # Update existing partition
            existing.record_count = record_count
            existing.size_bytes = size_bytes
            existing.file_count = file_count
            existing.last_updated = datetime.utcnow()
            self.db.commit()
            return existing
        
        # Create new partition
        partition = DataLakePartition(
            table_id=table_id,
            partition_path=partition_path,
            partition_values=partition_values,
            record_count=record_count,
            size_bytes=size_bytes,
            file_count=file_count
        )
        
        self.db.add(partition)
        self.db.commit()
        self.db.refresh(partition)
        
        logger.info(f"Created partition: {partition_path} for table {table_id}")
        return partition
    
    def _generate_partition_path(self, partition_values: Dict[str, Any]) -> str:
        """Generate partition path from values"""
        path_parts = []
        for key, value in sorted(partition_values.items()):
            if isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            path_parts.append(f"{key}={value}")
        return "/".join(path_parts)
    
    async def get_partition(
        self,
        table_id: int,
        partition_path: str
    ) -> Optional[DataLakePartition]:
        """Get a partition by table ID and path"""
        return self.db.query(DataLakePartition).filter(
            DataLakePartition.table_id == table_id,
            DataLakePartition.partition_path == partition_path
        ).first()
    
    async def list_partitions(
        self,
        table_id: int,
        limit: int = 100,
        offset: int = 0
    ) -> List[DataLakePartition]:
        """List partitions for a table"""
        return self.db.query(DataLakePartition).filter(
            DataLakePartition.table_id == table_id,
            DataLakePartition.is_active == True
        ).offset(offset).limit(limit).all()
    
    async def update_partition_stats(
        self,
        partition_id: int,
        record_count: int = None,
        size_bytes: int = None,
        file_count: int = None
    ) -> bool:
        """Update partition statistics"""
        partition = self.db.query(DataLakePartition).filter(
            DataLakePartition.id == partition_id
        ).first()
        
        if not partition:
            return False
        
        if record_count is not None:
            partition.record_count = record_count
        if size_bytes is not None:
            partition.size_bytes = size_bytes
        if file_count is not None:
            partition.file_count = file_count
        
        partition.last_updated = datetime.utcnow()
        self.db.commit()
        
        return True
    
    async def delete_partition(self, partition_id: int) -> bool:
        """Soft delete a partition"""
        partition = self.db.query(DataLakePartition).filter(
            DataLakePartition.id == partition_id
        ).first()
        
        if not partition:
            return False
        
        partition.is_active = False
        self.db.commit()
        
        logger.info(f"Deleted partition: {partition.partition_path}")
        return True
    
    async def get_partition_by_date_range(
        self,
        table_id: int,
        start_date: date,
        end_date: date
    ) -> List[DataLakePartition]:
        """Get partitions within a date range"""
        # This is a simplified implementation
        # In reality, you'd need to parse partition paths and filter by date
        
        partitions = self.db.query(DataLakePartition).filter(
            DataLakePartition.table_id == table_id,
            DataLakePartition.is_active == True
        ).all()
        
        # Filter by date range (simplified)
        filtered_partitions = []
        for partition in partitions:
            # Extract date from partition values
            partition_date = self._extract_date_from_partition(partition.partition_values)
            if partition_date and start_date <= partition_date <= end_date:
                filtered_partitions.append(partition)
        
        return filtered_partitions
    
    def _extract_date_from_partition(self, partition_values: Dict[str, Any]) -> Optional[date]:
        """Extract date from partition values"""
        # Look for common date fields
        date_fields = ["date", "year", "month", "day"]
        
        for field in date_fields:
            if field in partition_values:
                value = partition_values[field]
                if isinstance(value, date):
                    return value
                elif isinstance(value, str):
                    try:
                        return datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        continue
        
        return None
    
    async def optimize_partitions(
        self,
        table_id: int,
        min_size_mb: int = 128
    ) -> List[Dict[str, Any]]:
        """Optimize partitions by merging small ones"""
        
        table = self.db.query(DataLakeTable).filter(DataLakeTable.id == table_id).first()
        if not table:
            return []
        
        # Get small partitions
        min_size_bytes = min_size_mb * 1024 * 1024
        small_partitions = self.db.query(DataLakePartition).filter(
            DataLakePartition.table_id == table_id,
            DataLakePartition.size_bytes < min_size_bytes,
            DataLakePartition.is_active == True
        ).all()
        
        optimization_plan = []
        
        if small_partitions:
            # Group partitions by similar characteristics
            groups = self._group_partitions_for_optimization(small_partitions)
            
            for group in groups:
                if len(group) > 1:
                    optimization_plan.append({
                        "action": "merge",
                        "partitions": [p.id for p in group],
                        "estimated_savings": sum(p.size_bytes for p in group)
                    })
        
        return optimization_plan
    
    def _group_partitions_for_optimization(
        self,
        partitions: List[DataLakePartition]
    ) -> List[List[DataLakePartition]]:
        """Group partitions for optimization"""
        # Simplified grouping - in reality, you'd use more sophisticated logic
        groups = []
        
        # Group by similar partition values (excluding date)
        groups_by_prefix = {}
        
        for partition in partitions:
            # Create a key excluding date fields
            key_parts = []
            for k, v in partition.partition_values.items():
                if k not in ["date", "year", "month", "day"]:
                    key_parts.append(f"{k}={v}")
            
            key = "|".join(sorted(key_parts))
            
            if key not in groups_by_prefix:
                groups_by_prefix[key] = []
            groups_by_prefix[key].append(partition)
        
        # Return groups with more than one partition
        return [group for group in groups_by_prefix.values() if len(group) > 1]
