from typing import Dict, Any, Union
from datetime import date, datetime

def format_partition_path(partition_values: Dict[str, Any]) -> str:
    """Format partition values into a path string"""
    path_parts = []
    
    for key, value in sorted(partition_values.items()):
        if isinstance(value, (date, datetime)):
            if isinstance(value, datetime):
                value = value.date()
            value = value.strftime("%Y-%m-%d")
        elif isinstance(value, (int, float)):
            value = str(value)
        
        path_parts.append(f"{key}={value}")
    
    return "/".join(path_parts)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.2f} {size_names[i]}"

def format_duration(seconds: int) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"

def format_record_count(count: int) -> str:
    """Format record count in human readable format"""
    if count < 1000:
        return str(count)
    elif count < 1000000:
        return f"{count / 1000:.1f}K"
    elif count < 1000000000:
        return f"{count / 1000000:.1f}M"
    else:
        return f"{count / 1000000000:.1f}B"
