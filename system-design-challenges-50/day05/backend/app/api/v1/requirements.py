"""Requirements API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.requirement import RequirementCreate, RequirementUpdate, RequirementResponse
from app.services.requirement_service import RequirementService

router = APIRouter(prefix="/requirements", tags=["requirements"])

# Placeholder for dependency injection
def get_requirement_service():
    return RequirementService()

@router.post("/", response_model=RequirementResponse)
async def create_requirement(
    requirement: RequirementCreate,
    service: RequirementService = Depends(get_requirement_service)
):
    """Create a new requirement"""
    return await service.create_requirement(requirement)

@router.get("/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(
    requirement_id: int,
    service: RequirementService = Depends(get_requirement_service)
):
    """Get a requirement by ID"""
    req = await service.get_requirement(requirement_id)
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return req

@router.get("/", response_model=List[RequirementResponse])
async def list_requirements(
    skip: int = 0,
    limit: int = 100,
    service: RequirementService = Depends(get_requirement_service)
):
    """List requirements with pagination"""
    return await service.list_requirements(skip, limit)

@router.put("/{requirement_id}", response_model=RequirementResponse)
async def update_requirement(
    requirement_id: int,
    requirement: RequirementUpdate,
    service: RequirementService = Depends(get_requirement_service)
):
    """Update a requirement"""
    req = await service.update_requirement(requirement_id, requirement)
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return req

@router.delete("/{requirement_id}")
async def delete_requirement(
    requirement_id: int,
    service: RequirementService = Depends(get_requirement_service)
):
    """Delete a requirement"""
    success = await service.delete_requirement(requirement_id)
    if not success:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return {"message": "Requirement deleted successfully"}