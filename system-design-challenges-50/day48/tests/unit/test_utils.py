import pytest
from app.utils.validators import (
    validate_schema,
    validate_partition_values,
    validate_table_name,
    validate_partition_strategy,
    validate_storage_format,
    validate_compression
)
from app.utils.formatters import (
    format_partition_path,
    format_file_size,
    format_duration,
    format_record_count
)

class TestValidators:
    def test_validate_schema_valid(self):
        schema = {
            "fields": [
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
                {"name": "created_at", "type": "long"}
            ]
        }
        assert validate_schema(schema) == True
    
    def test_validate_schema_invalid(self):
        # Missing fields
        assert validate_schema({}) == False
        
        # Invalid field type
        schema = {
            "fields": [
                {"name": "id", "type": "invalid_type"}
            ]
        }
        assert validate_schema(schema) == False
    
    def test_validate_partition_values_valid(self):
        values = {"year": "2024", "month": "01", "day": "15"}
        assert validate_partition_values(values) == True
    
    def test_validate_partition_values_invalid(self):
        # Empty key
        values = {"": "value"}
        assert validate_partition_values(values) == False
    
    def test_validate_table_name(self):
        assert validate_table_name("valid_table_name") == True
        assert validate_table_name("valid-table-name") == True
        assert validate_table_name("valid_table_name_123") == True
        assert validate_table_name("123invalid") == False
        assert validate_table_name("") == False
        assert validate_table_name("invalid name") == False
    
    def test_validate_partition_strategy(self):
        assert validate_partition_strategy("date") == True
        assert validate_partition_strategy("hash") == True
        assert validate_partition_strategy("invalid") == False
    
    def test_validate_storage_format(self):
        assert validate_storage_format("parquet") == True
        assert validate_storage_format("avro") == True
        assert validate_storage_format("invalid") == False
    
    def test_validate_compression(self):
        assert validate_compression("snappy") == True
        assert validate_compression("gzip") == True
        assert validate_compression("invalid") == False

class TestFormatters:
    def test_format_partition_path(self):
        values = {"year": "2024", "month": "01", "day": "15"}
        result = format_partition_path(values)
        assert result == "day=15/month=01/year=2024"
    
    def test_format_file_size(self):
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.00 KB"
        assert format_file_size(1048576) == "1.00 MB"
        assert format_file_size(1073741824) == "1.00 GB"
    
    def test_format_duration(self):
        assert format_duration(30) == "30s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(3661) == "1h 1m"
    
    def test_format_record_count(self):
        assert format_record_count(500) == "500"
        assert format_record_count(1500) == "1.5K"
        assert format_record_count(1500000) == "1.5M"
        assert format_record_count(1500000000) == "1.5B"
