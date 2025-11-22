import uuid
import secrets
from typing import Optional


def generate_uuid() -> str:
    """
    Generate a UUID4 string.
    
    Returns:
        str: UUID4 string
    """
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """
    Generate a short random ID.
    
    Args:
        length: Length of the ID
        
    Returns:
        str: Short random ID
    """
    return secrets.token_hex(length // 2)


def generate_ulid() -> str:
    """
    Generate a ULID (Universally Unique Lexicographically Sortable Identifier).
    
    Returns:
        str: ULID string
    """
    # Simplified ULID implementation using timestamp + random
    import time
    timestamp = int(time.time() * 1000)  # 48-bit timestamp
    random_part = secrets.token_hex(16)  # 80-bit random
    
    # Combine timestamp and random parts
    return f"{timestamp:x}{random_part}"


def generate_entity_id(prefix: Optional[str] = None) -> str:
    """
    Generate an entity ID with optional prefix.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        str: Entity ID
    """
    base_id = generate_short_id(12)
    if prefix:
        return f"{prefix}_{base_id}"
    return base_id


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if a string is a valid UUID.
    
    Args:
        uuid_string: String to check
        
    Returns:
        bool: True if valid UUID
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False