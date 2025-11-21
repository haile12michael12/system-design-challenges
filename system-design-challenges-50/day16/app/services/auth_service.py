from sqlalchemy.orm import Session
from datetime import timedelta
from ..db.models.user import User
from ..schemas.auth import UserCreate, UserLogin, Token
from ..schemas.user import User as UserSchema
from ..core.security import get_password_hash, verify_password, create_access_token
from ..core.config import settings
from ..core.exceptions import InvalidCredentialsException, UserAlreadyExistsException

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user: UserCreate) -> UserSchema:
        """Register a new user."""
        # Check if user already exists
        db_user = self.db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        
        if db_user:
            raise UserAlreadyExistsException()
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return UserSchema.from_orm(db_user)

    def authenticate_user(self, user: UserLogin) -> Token:
        """Authenticate a user and return access token."""
        db_user = self.db.query(User).filter(User.username == user.username).first()
        
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise InvalidCredentialsException()
        
        # Create access and refresh tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=refresh_token_expires
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )