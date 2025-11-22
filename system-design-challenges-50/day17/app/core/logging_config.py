import logging
import sys
from typing import Optional

from .config import settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Set up logging configuration."""
    if log_level is None:
        log_level = "INFO"
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Configure application logger
    app_logger = logging.getLogger("feed_service")
    app_logger.setLevel(log_level)
    app_logger.addHandler(console_handler)
    
    # If in development, set higher log level for third-party libraries
    if settings.ENVIRONMENT == "development":
        logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
        logging.getLogger("uvicorn").setLevel(logging.WARNING)


# Default logger for the application
logger = logging.getLogger("feed_service")