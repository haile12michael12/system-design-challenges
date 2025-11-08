from fastapi import HTTPException, status

class LoggingPipelineException(Exception):
    """Base exception for the logging pipeline"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationError(LoggingPipelineException):
    """Raised when log data fails validation"""
    pass

class DatabaseError(LoggingPipelineException):
    """Raised when database operations fail"""
    pass

class RedisError(LoggingPipelineException):
    """Raised when Redis operations fail"""
    pass

class AuthenticationError(LoggingPipelineException):
    """Raised when authentication fails"""
    pass

class AuthorizationError(LoggingPipelineException):
    """Raised when authorization fails"""
    pass

class LogIngestionError(LoggingPipelineException):
    """Raised when log ingestion fails"""
    pass

# HTTP exceptions
class InvalidAPIKeyException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

class LogValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

class LogNotFoundException(HTTPException):
    def __init__(self, log_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log with ID {log_id} not found",
        )