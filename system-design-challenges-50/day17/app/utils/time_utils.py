from datetime import datetime, timedelta
from typing import Optional
import time


def get_current_timestamp() -> int:
    """
    Get current timestamp in seconds.
    
    Returns:
        int: Current timestamp
    """
    return int(time.time())


def get_current_datetime() -> datetime:
    """
    Get current datetime in UTC.
    
    Returns:
        datetime: Current datetime
    """
    return datetime.utcnow()


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime to format
        format_str: Format string
        
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse datetime from string.
    
    Args:
        date_str: Datetime string
        format_str: Format string
        
    Returns:
        datetime: Parsed datetime
    """
    return datetime.strptime(date_str, format_str)


def get_time_range(days: int = 7) -> tuple:
    """
    Get a time range from now to N days ago.
    
    Args:
        days: Number of days
        
    Returns:
        tuple: (start_time, end_time) as timestamps
    """
    end_time = get_current_timestamp()
    start_time = end_time - (days * 24 * 60 * 60)
    return start_time, end_time


def is_within_time_range(timestamp: int, hours: int = 24) -> bool:
    """
    Check if a timestamp is within the last N hours.
    
    Args:
        timestamp: Timestamp to check
        hours: Number of hours
        
    Returns:
        bool: True if within range
    """
    current_time = get_current_timestamp()
    return current_time - timestamp <= hours * 60 * 60


def get_expiration_time(hours: int = 1) -> datetime:
    """
    Get expiration time N hours from now.
    
    Args:
        hours: Number of hours
        
    Returns:
        datetime: Expiration time
    """
    return get_current_datetime() + timedelta(hours=hours)