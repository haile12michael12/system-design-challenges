from jose import JWTError, jwt
from datetime import datetime
from typing import Optional
from .config import settings

def decode_access_token(token: str) -> Optional[dict]:
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def is_token_expired(payload: dict) -> bool:
    """Check if a token is expired."""
    expire = payload.get("exp")
    if expire is None:
        return True
    return datetime.utcnow() > datetime.fromtimestamp(expire)