import logging
import json
from typing import Any, Dict
import sys

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, 
                   message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp
        if 'timestamp' not in log_record:
            log_record['timestamp'] = self.formatTime(record, self.datefmt)
            
        # Add level
        if 'level' not in log_record:
            log_record['level'] = record.levelname
            
        # Add logger name
        if 'logger' not in log_record:
            log_record['logger'] = record.name


def setup_logging(level: int = logging.INFO) -> None:
    """Set up structured JSON logging"""
    # Create formatter
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    
    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance"""
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, exception: Exception, context: str = "") -> None:
    """Log an exception with context"""
    logger.error(
        f"Exception in {context}: {str(exception)}",
        extra={
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "context": context
        }
    )