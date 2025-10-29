from typing import Dict, Any, List, Optional
import json
import re

def validate_schema(schema_definition: Dict[str, Any]) -> bool:
    """Validate a schema definition"""
    try:
        # Check required fields
        if "fields" not in schema_definition:
            return False
        
        fields = schema_definition["fields"]
        if not isinstance(fields, list):
            return False
        
        # Validate each field
        for field in fields:
            if not isinstance(field, dict):
                return False
            
            # Required field properties
            if "name" not in field or "type" not in field:
                return False
            
            # Validate field name
            if not isinstance(field["name"], str) or not field["name"]:
                return False
            
            # Validate field type
            valid_types = ["string", "integer", "long", "float", "double", "boolean", "bytes", "record", "array", "map", "union", "null"]
            if field["type"] not in valid_types:
                return False
        
        return True
        
    except Exception:
        return False

def validate_partition_values(partition_values: Dict[str, Any]) -> bool:
    """Validate partition values"""
    try:
        # Check that all values are strings or can be converted to strings
        for key, value in partition_values.items():
            if not isinstance(key, str) or not key:
                return False
            
            # Value should be serializable
            json.dumps(value)
        
        return True
        
    except Exception:
        return False

def validate_table_name(name: str) -> bool:
    """Validate table name"""
    if not name or not isinstance(name, str):
        return False
    
    # Check for valid characters (alphanumeric, underscore, hyphen)
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, name))

def validate_partition_strategy(strategy: str) -> bool:
    """Validate partition strategy"""
    valid_strategies = ["date", "hash", "range", "list"]
    return strategy in valid_strategies

def validate_storage_format(format_name: str) -> bool:
    """Validate storage format"""
    valid_formats = ["parquet", "avro", "json", "csv", "orc"]
    return format_name in valid_formats

def validate_compression(compression: str) -> bool:
    """Validate compression type"""
    valid_compressions = ["none", "snappy", "gzip", "lz4", "zstd"]
    return compression in valid_compressions
