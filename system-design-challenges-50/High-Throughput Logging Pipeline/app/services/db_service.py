from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from typing import List, Optional
from app.db.models import LogEntry, Tenant
from app.schemas.logs import LogIn, LogLevel
from app.schemas.query import LogQueryParams
from app.core.config import settings
from app.core.logging_config import get_logger
import uuid
from datetime import datetime

logger = get_logger("db_service")

class DBService:
    @staticmethod
    async def create_log_entry(db: AsyncSession, log_data: LogIn) -> LogEntry:
        """
        Create a single log entry in the database
        """
        try:
            db_log = LogEntry(
                id=str(uuid.uuid4()),
                timestamp=log_data.timestamp,
                level=log_data.level,
                message=log_data.message,
                service=log_data.service,
                tenant_id=log_data.tenant_id,
                trace_id=log_data.trace_id,
                span_id=log_data.span_id,
                metadata_=log_data.metadata
            )
            db.add(db_log)
            await db.commit()
            await db.refresh(db_log)
            logger.info(f"Created log entry: {db_log.id}")
            return db_log
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create log entry: {str(e)}")
            raise
            
    @staticmethod
    async def create_log_entries_batch(db: AsyncSession, logs_data: List[LogIn]) -> List[LogEntry]:
        """
        Create multiple log entries in the database in a batch
        """
        try:
            db_logs = []
            for log_data in logs_data:
                db_log = LogEntry(
                    id=str(uuid.uuid4()),
                    timestamp=log_data.timestamp,
                    level=log_data.level,
                    message=log_data.message,
                    service=log_data.service,
                    tenant_id=log_data.tenant_id,
                    trace_id=log_data.trace_id,
                    span_id=log_data.span_id,
                    metadata_=log_data.metadata
                )
                db_logs.append(db_log)
                
            db.add_all(db_logs)
            await db.commit()
            
            # Refresh all entries to get their IDs
            for db_log in db_logs:
                await db.refresh(db_log)
                
            logger.info(f"Created batch of {len(db_logs)} log entries")
            return db_logs
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create batch of log entries: {str(e)}")
            raise
            
    @staticmethod
    async def query_logs(db: AsyncSession, query_params: LogQueryParams) -> List[LogEntry]:
        """
        Query log entries with filters
        """
        try:
            query = select(LogEntry)
            
            # Apply filters
            filters = []
            if query_params.service:
                filters.append(LogEntry.service == query_params.service)
            if query_params.tenant_id:
                filters.append(LogEntry.tenant_id == query_params.tenant_id)
            if query_params.level:
                filters.append(LogEntry.level == query_params.level)
            if query_params.start_time:
                filters.append(LogEntry.timestamp >= query_params.start_time)
            if query_params.end_time:
                filters.append(LogEntry.timestamp <= query_params.end_time)
                
            if filters:
                query = query.where(and_(*filters))
                
            # Apply ordering and pagination
            query = query.order_by(desc(LogEntry.timestamp))
            query = query.offset(query_params.offset).limit(query_params.limit)
            
            result = await db.execute(query)
            logs = result.scalars().all()
            logger.info(f"Queried {len(logs)} log entries")
            return logs
        except Exception as e:
            logger.error(f"Failed to query log entries: {str(e)}")
            raise
            
    @staticmethod
    async def get_log_count(db: AsyncSession, query_params: LogQueryParams) -> int:
        """
        Get the count of log entries matching the query
        """
        try:
            query = select(func.count(LogEntry.id))
            
            # Apply filters
            filters = []
            if query_params.service:
                filters.append(LogEntry.service == query_params.service)
            if query_params.tenant_id:
                filters.append(LogEntry.tenant_id == query_params.tenant_id)
            if query_params.level:
                filters.append(LogEntry.level == query_params.level)
            if query_params.start_time:
                filters.append(LogEntry.timestamp >= query_params.start_time)
            if query_params.end_time:
                filters.append(LogEntry.timestamp <= query_params.end_time)
                
            if filters:
                query = query.where(and_(*filters))
                
            result = await db.execute(query)
            count = result.scalar()
            return count or 0
        except Exception as e:
            logger.error(f"Failed to get log count: {str(e)}")
            raise