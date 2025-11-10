"""
Logging Configuration
"""
import logging
import sys
from typing import Optional
from app.core.config import settings

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Setup structured logging"""
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Global logger instance
logger = setup_logging()