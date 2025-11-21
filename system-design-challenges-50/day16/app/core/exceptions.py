from fastapi import HTTPException, status

class AuthException(HTTPException):
    """Base authentication exception."""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class InvalidCredentialsException(AuthException):
    """Exception raised for invalid credentials."""
    def __init__(self):
        super().__init__("Invalid credentials")

class UserAlreadyExistsException(HTTPException):
    """Exception raised when user already exists."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

class TokenExpiredException(AuthException):
    """Exception raised when token is expired."""
    def __init__(self):
        super().__init__("Token has expired")

class InvalidTokenException(AuthException):
    """Exception raised for invalid token."""
    def __init__(self):
        super().__init__("Invalid token")