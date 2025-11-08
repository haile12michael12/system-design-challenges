from datetime import datetime, timezone
from typing import Optional
import re

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

def convert_to_utc(dt: datetime) -> datetime:
    """
    Convert datetime to UTC
    """
    if dt.tzinfo is None:
        # Assume naive datetime is in local timezone
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def is_within_retention_period(dt: datetime, retention_days: int) -> bool:
    """
    Check if a datetime is within the retention period
    """
    cutoff_date = get_current_utc_time() - timedelta(days=retention_days)
    return dt >= cutoff_date

def parse_iso_datetime(iso_str: str) -> datetime:
    """
    Parse ISO format datetime string
    """
    # Handle different ISO formats
    iso_formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S"
    ]
    
    for fmt in iso_formats:
        try:
            return datetime.strptime(iso_str, fmt)
        except ValueError:
            continue
            
    raise ValueError(f"Unable to parse datetime string: {iso_str}")