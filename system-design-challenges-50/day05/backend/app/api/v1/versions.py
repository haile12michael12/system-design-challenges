"""Versions API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.version import VersionCreate, VersionUpdate, VersionResponse
from app.services.version_service import VersionService

router = APIRouter(prefix="/versions", tags=["versions"])

# Placeholder for dependency injection
def get_version_service():
    return VersionService()

@router.post("/", response_model=VersionResponse)
async def create_version(
    version: VersionCreate,
    service: VersionService = Depends(get_version_service)
):
    """Create a new version"""
    return await service.create_version(version)

@router.get("/{version_id}", response_model=VersionResponse)
async def get_version(
    version_id: int,
    service: VersionService = Depends(get_version_service)
):
    """Get a version by ID"""
    version = await service.get_version(version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version

@router.get("/requirement/{requirement_id}", response_model=List[VersionResponse])
async def list_versions(
    requirement_id: int,
    service: VersionService = Depends(get_version_service)
):
    """List versions for a requirement"""
    return await service.list_versions(requirement_id)

@router.put("/{version_id}", response_model=VersionResponse)
async def update_version(
    version_id: int,
    version: VersionUpdate,
    service: VersionService = Depends(get_version_service)
):
    """Update a version"""
    updated_version = await service.update_version(version_id, version)
    if not updated_version:
        raise HTTPException(status_code=404, detail="Version not found")
    return updated_version

@router.delete("/{version_id}")
async def delete_version(
    version_id: int,
    service: VersionService = Depends(get_version_service)
):
    """Delete a version"""
    success = await service.delete_version(version_id)
    if not success:
        raise HTTPException(status_code=404, detail="Version not found")
    return {"message": "Version deleted successfully"}