import logging
import sys
from .config import settings

def setup_logging() -> logging.Logger:
    """Set up application logging."""
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Create a default logger
logger = setup_logging()