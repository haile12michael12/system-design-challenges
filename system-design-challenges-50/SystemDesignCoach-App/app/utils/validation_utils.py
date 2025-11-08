import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_username(username: str) -> bool:
    """
    Validate username format (alphanumeric and underscores, 3-20 characters)
    """
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> bool:
    """
    Validate password strength (at least 8 characters, with letters and numbers)
    """
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

def validate_diagram_syntax(diagram_data: str, diagram_type: str) -> bool:
    """
    Validate diagram syntax based on type (Mermaid, PlantUML, etc.)
    """
    # Placeholder implementation - in practice, you would use specific
    # parsers for each diagram type
    if diagram_type.lower() == "mermaid":
        return "graph" in diagram_data or "sequenceDiagram" in diagram_data
    elif diagram_type.lower() == "plantuml":
        return "@startuml" in diagram_data and "@enduml" in diagram_data
    return len(diagram_data) > 0

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent XSS attacks
    """
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', input_str)
    # Limit length
    return sanitized[:1000]