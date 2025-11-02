"""Projects API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])

# In-memory storage for projects (placeholder)
projects_db = {}
projects_counter = 0

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """Create a new project"""
    global projects_counter
    projects_counter += 1
    project_data = project.dict()
    project_data["id"] = projects_counter
    project_data["created_at"] = "2025-01-01T00:00:00"
    project_data["updated_at"] = "2025-01-01T00:00:00"
    projects_db[projects_counter] = project_data
    return project_data

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """Get a project by ID"""
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(skip: int = 0, limit: int = 100):
    """List projects with pagination"""
    projects = list(projects_db.values())[skip:skip+limit]
    return projects

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate):
    """Update a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = projects_db[project_id]
    update_data = project.dict(exclude_unset=True)
    project_data.update(update_data)
    project_data["updated_at"] = "2025-01-01T00:00:00"
    projects_db[project_id] = project_data
    return project_data

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """Delete a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    del projects_db[project_id]
    return {"message": "Project deleted successfully"}