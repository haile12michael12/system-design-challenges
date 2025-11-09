import logging
import json
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """
    Custom formatter to output logs in JSON format
    """
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields if present in __dict__
        for key, value in record.__dict__.items():
            if key not in log_entry and not key.startswith('_'):
                log_entry[key] = value
            
        return json.dumps(log_entry)

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the application
    """
    # Create formatter
    formatter = JSONFormatter()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Configure application logger
    app_logger = logging.getLogger("doc_editor")
    app_logger.setLevel(level)
    app_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    """
    return logging.getLogger(f"doc_editor.{name}")