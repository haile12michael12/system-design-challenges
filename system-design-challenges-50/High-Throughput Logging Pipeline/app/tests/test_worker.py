import pytest
from app.workers.retry_handler import RetryHandler
from app.services.redis_service import RedisService
from app.utils.compression_utils import compress_log_data, decompress_log_data

def test_retry_handler():
    """
    Test the retry handler
    """
    retry_handler = RetryHandler(max_retries=3, base_delay=0.1)
    
    # Test successful function
    def successful_func():
        return "success"
        
    result = retry_handler.execute_with_retry_sync(successful_func)
    assert result == "success"

def test_compression_utils():
    """
    Test compression utilities
    """
    # Test with dictionary
    log_data = {"message": "test log", "level": "INFO"}
    compressed = compress_log_data(log_data)
    decompressed = decompress_log_data(compressed)
    assert decompressed == log_data
    
    # Test with string
    log_str = "test log message"
    compressed = compress_log_data(log_str)
    decompressed = decompress_log_data(compressed)
    assert decompressed == log_str

def test_redis_service_import():
    """
    Test that RedisService can be imported
    """
    # This test just verifies that the import works
    # In a real test, we would mock Redis
    assert RedisService is not None