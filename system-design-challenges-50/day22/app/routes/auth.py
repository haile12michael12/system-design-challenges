from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserResponse
from app.services.auth_service import authenticate_user, create_access_token, register_user
from app.db.session import get_db

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register_new_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return user