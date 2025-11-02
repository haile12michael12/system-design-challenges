"""Logging configuration"""
import logging
import sys
from typing import Optional

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up application logging"""
    logger = logging.getLogger("requirements_tracker")
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

# Global logger instance
logger = setup_logging()