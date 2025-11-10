"""
Utility Functions
"""
import hashlib
import uuid
from typing import Any, Dict
from datetime import datetime

def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())

def hash_data(data: str) -> str:
    """Hash data using SHA256"""
    return hashlib.sha256(data.encode()).hexdigest()

def serialize_model(model: Any) -> Dict:
    """Serialize a SQLAlchemy model to dictionary"""
    if hasattr(model, '__dict__'):
        data = {}
        for key, value in model.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                else:
                    data[key] = value
        return data
    return {}

def paginate_query(query_result: list, limit: int, offset: int) -> Dict:
    """Paginate a query result"""
    total = len(query_result)
    paginated = query_result[offset:offset + limit]
    
    return {
        "data": paginated,
        "total": total,
        "limit": limit,
        "offset": offset
    }