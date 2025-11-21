import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt
from ..core.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create an access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_api_key() -> str:
    """Generate a new API key"""
    return secrets.token_urlsafe(32)