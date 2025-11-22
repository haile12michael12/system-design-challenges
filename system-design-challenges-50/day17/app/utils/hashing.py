import hashlib
import secrets
from typing import Tuple


def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    """
    Hash a password with a salt.
    
    Args:
        password: Password to hash
        salt: Optional salt (generated if not provided)
        
    Returns:
        Tuple[str, str]: Hashed password and salt
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Create hash using SHA-256
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    hashed_password = hash_obj.hex()
    
    return hashed_password, salt


def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a password against its hash and salt.
    
    Args:
        password: Password to verify
        hashed_password: Hashed password
        salt: Salt used for hashing
        
    Returns:
        bool: True if password matches
    """
    new_hashed_password, _ = hash_password(password, salt)
    return new_hashed_password == hashed_password


def generate_token() -> str:
    """
    Generate a secure random token.
    
    Returns:
        str: Random token
    """
    return secrets.token_urlsafe(32)


def hash_content(content: str) -> str:
    """
    Create a hash of content for deduplication or integrity checking.
    
    Args:
        content: Content to hash
        
    Returns:
        str: Hash of the content
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()