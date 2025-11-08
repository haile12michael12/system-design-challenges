from datetime import datetime, timezone
from typing import Optional

def get_current_utc_time() -> datetime:
    """
    Get current UTC time
    """
    return datetime.now(timezone.utc)

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string
    """
    return dt.strftime(format_str)

def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse string to datetime
    """
    return datetime.strptime(date_str, format_str)

def get_days_since(start_date: datetime) -> int:
    """
    Calculate days since a given date
    """
    delta = datetime.now(timezone.utc) - start_date
    return delta.days

def is_recent_date(date: datetime, hours: int = 24) -> bool:
    """
    Check if a date is within the last N hours
    """
    delta = datetime.now(timezone.utc) - date
    return delta.total_seconds() <= hours * 3600