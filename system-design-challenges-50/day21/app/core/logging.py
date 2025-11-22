import logging
import sys
from typing import Optional
import json
from datetime import datetime

from app.core.config import settings


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Set up application logging"""
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger("social_media_app")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


def log_request_info(method: str, url: str, status_code: int, 
                    duration: float, user_id: Optional[str] = None) -> None:
    """Log request information"""
    logger = logging.getLogger("social_media_app.request")
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "url": url,
        "status_code": status_code,
        "duration_ms": round(duration * 1000, 2),
        "user_id": user_id
    }
    
    logger.info(f"Request: {json.dumps(log_data)}")


def log_error_info(error_type: str, error_message: str, 
                  traceback: Optional[str] = None, user_id: Optional[str] = None) -> None:
    """Log error information"""
    logger = logging.getLogger("social_media_app.error")
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": error_type,
        "error_message": error_message,
        "traceback": traceback,
        "user_id": user_id
    }
    
    logger.error(f"Error: {json.dumps(log_data)}")


# Initialize logger
logger = setup_logging()