from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Mock data storage
users = []

@router.get("/", response_model=list[User])
async def list_users(skip: int = 0, limit: int = 100):
    """List all users"""
    return users[skip : skip + limit]

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    new_user = User(
        id=len(users) + 1,
        **user.dict(exclude={"password"}),
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    users.append(new_user)
    return new_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a user by ID"""
    for user in users:
        if user.id == user_id:
            return user
    return {"error": "User not found"}

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserBase):
    """Update a user"""
    for user in users:
        if user.id == user_id:
            user.username = user_update.username
            user.email = user_update.email
            user.full_name = user_update.full_name
            user.updated_at = datetime.now()
            return user
    return {"error": "User not found"}