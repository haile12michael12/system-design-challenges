import hashlib
import hmac
import secrets
from typing import Optional
from app.core.config import settings

def generate_api_key() -> str:
    """
    Generate a secure API key
    """
    return secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for secure storage
    """
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(provided_key: str, stored_hash: Optional[str] = None) -> bool:
    """
    Verify an API key against a stored hash
    """
    # In a real implementation, you would:
    # 1. Hash the provided key
    # 2. Compare with the stored hash
    # 3. Return True if they match
    
    # For now, we'll use a simple check against the config
    if stored_hash:
        return hmac.compare_digest(hash_api_key(provided_key), stored_hash)
    
    # Fallback to config-based verification for development
    return provided_key == settings.API_KEY

def generate_jwt_token(payload: dict, secret_key: str = None) -> str:
    """
    Generate a JWT token (simplified implementation)
    """
    import jwt
    from datetime import datetime, timedelta
    
    if secret_key is None:
        secret_key = settings.SECRET_KEY
        
    # Add expiration
    payload['exp'] = datetime.utcnow() + timedelta(hours=1)
    
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_jwt_token(token: str, secret_key: str = None) -> dict:
    """
    Verify a JWT token (simplified implementation)
    """
    import jwt
    
    if secret_key is None:
        secret_key = settings.SECRET_KEY
        
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")