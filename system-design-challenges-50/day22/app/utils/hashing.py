import hashlib
import secrets

def hash_content(content: str) -> str:
    """Generate SHA-256 hash of content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)

def verify_hash(content: str, hash_value: str) -> bool:
    """Verify content against its hash"""
    return hash_content(content) == hash_value

def hash_password(password: str) -> str:
    """Hash a password with salt"""
    # In a real implementation, we would use a proper password hashing library
    # like bcrypt or argon2. This is a simplified version for demonstration.
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${hashed.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, stored_hash = hashed_password.split('$')
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return hashed.hex() == stored_hash
    except Exception:
        return False