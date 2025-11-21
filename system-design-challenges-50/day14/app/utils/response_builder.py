from typing import Any, Dict, Optional

def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create a success response"""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response

def error_response(message: str, status_code: int = 500, details: Any = None) -> Dict[str, Any]:
    """Create an error response"""
    response = {"success": False, "message": message, "status_code": status_code}
    if details is not None:
        response["details"] = details
    return response

def paginated_response(items: list, total: int, page: int, size: int, message: str = "Success") -> Dict[str, Any]:
    """Create a paginated response"""
    return {
        "success": True,
        "message": message,
        "data": {
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size
            }
        }
    }