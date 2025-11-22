from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

from .logging_config import logger


class FeedServiceException(Exception):
    """Base exception class for the Feed Service."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class PostNotFoundException(FeedServiceException):
    """Exception raised when a post is not found."""
    def __init__(self, post_id: str):
        super().__init__(f"Post with ID {post_id} not found", 404)


class UserNotFoundException(FeedServiceException):
    """Exception raised when a user is not found."""
    def __init__(self, user_id: str):
        super().__init__(f"User with ID {user_id} not found", 404)


class UnauthorizedException(FeedServiceException):
    """Exception raised when a user is not authorized."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class ValidationException(FeedServiceException):
    """Exception raised when validation fails."""
    def __init__(self, message: str):
        super().__init__(message, 400)


def setup_exception_handlers(app: "fastapi.FastAPI") -> None:
    """Set up global exception handlers for the application."""
    
    @app.exception_handler(FeedServiceException)
    async def feed_service_exception_handler(request: Request, exc: FeedServiceException):
        """Handle FeedServiceException."""
        logger.error(f"FeedServiceException: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTPException."""
        logger.error(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred"}
        )