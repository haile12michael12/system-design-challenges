import logging
import sys
from typing import Optional

from .config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Set up logging configuration."""
    if log_level is None:
        log_level = "DEBUG" if settings.DEBUG else "INFO"
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set specific log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)


# Create a logger instance that can be imported and used throughout the application
logger = logging.getLogger("feed_service")