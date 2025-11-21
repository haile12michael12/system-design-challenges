class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(AppException):
    """Validation error"""
    def __init__(self, message: str):
        super().__init__(message, 400)

class AuthenticationError(AppException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, 401)

class AuthorizationError(AppException):
    """Authorization error"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)

class NotFoundError(AppException):
    """Resource not found error"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class ConflictError(AppException):
    """Resource conflict error"""
    def __init__(self, message: str):
        super().__init__(message, 409)