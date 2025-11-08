import gzip
import json
from typing import Union, Dict, List

def compress_log_data(log_data: Union[Dict, List, str]) -> bytes:
    """
    Compress log data using gzip
    """
    # Convert to JSON string if needed
    if isinstance(log_data, (dict, list)):
        log_str = json.dumps(log_data)
    else:
        log_str = log_data
        
    # Convert to bytes if needed
    if isinstance(log_str, str):
        log_bytes = log_str.encode('utf-8')
    else:
        log_bytes = log_str
        
    # Compress using gzip
    compressed_data = gzip.compress(log_bytes)
    return compressed_data

def decompress_log_data(compressed_data: bytes) -> Union[Dict, List, str]:
    """
    Decompress log data using gzip
    """
    # Decompress using gzip
    decompressed_bytes = gzip.decompress(compressed_data)
    
    # Convert to string
    log_str = decompressed_bytes.decode('utf-8')
    
    # Try to parse as JSON, fallback to string
    try:
        log_data = json.loads(log_str)
        return log_data
    except json.JSONDecodeError:
        return log_str

def is_compressed(data: bytes) -> bool:
    """
    Check if data is gzip compressed
    """
    return data.startswith(b'\x1f\x8b')