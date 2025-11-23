import logging
import json
from datetime import datetime
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                              'filename', 'module', 'lineno', 'funcName', 'created', 
                              'msecs', 'relativeCreated', 'thread', 'threadName', 
                              'processName', 'process', 'exc_info', 'exc_text', 'stack_info']:
                    log_entry[key] = value
        
        return json.dumps(log_entry)

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up structured JSON logging"""
    # Create logger
    logger = logging.getLogger("feed_engine")
    logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

def log_request_info(method: str, url: str, status_code: int, duration: float):
    """Log HTTP request information"""
    logger = logging.getLogger("feed_engine.request")
    logger.info("HTTP request", extra={
        "http_method": method,
        "url": url,
        "status_code": status_code,
        "duration_ms": duration
    })

def log_error_info(error_type: str, message: str, details: Dict[str, Any] = None):
    """Log error information"""
    logger = logging.getLogger("feed_engine.error")
    logger.error(message, extra={
        "error_type": error_type,
        "details": details or {}
    })