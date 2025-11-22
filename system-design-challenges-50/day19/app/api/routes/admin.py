from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
import os

from app.api.deps import verify_admin_access
from app.services.wal_service import WALService
from app.services.replication_service import ReplicationService
from app.db.models import WALRecord

router = APIRouter()


@router.get("/replicas/status")
async def get_replica_status(current_user: dict = Depends(verify_admin_access)):
    """Get status of all replicas"""
    try:
        replication_service = ReplicationService()
        status = replication_service.get_replica_status()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get replica status: {str(e)}"
        )


@router.get("/wal/segments")
async def list_wal_segments(current_user: dict = Depends(verify_admin_access)):
    """List all WAL segments"""
    try:
        wal_service = WALService()
        segments = wal_service.list_segments()
        return {"segments": segments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list WAL segments: {str(e)}"
        )


@router.get("/wal/entries")
async def list_wal_entries(
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(verify_admin_access)
):
    """List WAL entries"""
    try:
        wal_service = WALService()
        entries = wal_service.get_entries(limit=limit, offset=offset)
        return {"entries": entries}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list WAL entries: {str(e)}"
        )


@router.post("/replicas/sync")
async def force_replica_sync(current_user: dict = Depends(verify_admin_access)):
    """Force synchronization of all replicas"""
    try:
        replication_service = ReplicationService()
        result = replication_service.sync_all_replicas()
        return {"message": "Replica synchronization initiated", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate replica sync: {str(e)}"
        )


@router.get("/wal/inspect/{segment_id}")
async def inspect_wal_segment(segment_id: str, current_user: dict = Depends(verify_admin_access)):
    """Inspect a specific WAL segment"""
    try:
        wal_service = WALService()
        segment_info = wal_service.inspect_segment(segment_id)
        return segment_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to inspect WAL segment: {str(e)}"
        )