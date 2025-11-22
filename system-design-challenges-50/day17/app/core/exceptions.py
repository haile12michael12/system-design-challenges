from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""
    pass


class UserNotFoundError(AppException):
    """Raised when a user is not found."""
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )


class PostNotFoundError(AppException):
    """Raised when a post is not found."""
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found"
        )


class UnauthorizedError(AppException):
    """Raised when user is not authorized."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )


class ValidationError(AppException):
    """Raised when there's a validation error."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )