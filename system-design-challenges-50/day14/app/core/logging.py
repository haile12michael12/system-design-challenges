import logging
import sys
from datetime import datetime

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

def log_event(event_type: str, details: dict = None):
    """Log an application event"""
    logger = setup_logging()
    details_str = f" - Details: {details}" if details else ""
    logger.info(f"Event: {event_type}{details_str}")

def log_error(error_type: str, error_message: str, details: dict = None):
    """Log an error event"""
    logger = setup_logging()
    details_str = f" - Details: {details}" if details else ""
    logger.error(f"Error: {error_type} - {error_message}{details_str}")