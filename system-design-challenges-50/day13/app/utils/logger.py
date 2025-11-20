import logging
import sys
from datetime import datetime

def setup_logger(name: str, level: int = logging.INFO):
    """Set up a logger with the specified name and level"""
    logger = logging.getLogger(name)
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

def log_payment_event(event_type: str, payment_id: int, details: dict = None):
    """Log a payment event"""
    logger = setup_logger("payment_events")
    details_str = f" - Details: {details}" if details else ""
    logger.info(f"Payment Event: {event_type} - Payment ID: {payment_id}{details_str}")

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:.2f}"
    return f"{amount:.2f} {currency}"