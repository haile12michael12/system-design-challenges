from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.auth import UserCreate, UserLogin, Token
from ..schemas.user import User
from ..services.auth_service import AuthService
from ..services.token_service import TokenService
from ..db.session import get_db

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    auth_service = AuthService(db)
    return auth_service.register_user(user)

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login a user and return access token."""
    auth_service = AuthService(db)
    return auth_service.authenticate_user(user)

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    token_service = TokenService(db)
    return token_service.refresh_access_token(refresh_token)

@router.post("/logout")
def logout_user(token: str, db: Session = Depends(get_db)):
    """Logout a user by revoking token."""
    token_service = TokenService(db)
    token_service.revoke_token(token)
    return {"message": "Successfully logged out"}