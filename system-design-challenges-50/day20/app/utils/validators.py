import re
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)


def validate_service_id(service_id: str) -> bool:
    """Validate service ID format"""
    if not service_id:
        return False
    
    # Service ID should be alphanumeric with hyphens, 1-100 characters
    pattern = r'^[a-zA-Z0-9\-_]{1,100}$'
    return bool(re.match(pattern, service_id))


def validate_metric_names(metric_names: List[str]) -> bool:
    """Validate metric names"""
    if not metric_names:
        return False
    
    # Metric names should be alphanumeric with underscores, dots, 1-100 characters
    pattern = r'^[a-zA-Z0-9_\.\-]{1,100}$'
    return all(re.match(pattern, name) for name in metric_names)


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range"""
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # End date should be after start date
        if end <= start:
            return False
        
        # Date range should not exceed 365 days
        if (end - start).days > 365:
            return False
            
        return True
    except ValueError:
        return False


def validate_priority(priority: int) -> bool:
    """Validate priority level (1-5)"""
    return 1 <= priority <= 5


def validate_budget_constraints(constraints: Dict[str, Any]) -> bool:
    """Validate budget constraints"""
    if not constraints:
        return True  # Optional field
    
    # Check required fields
    required_fields = ['max_monthly_spend', 'currency']
    for field in required_fields:
        if field not in constraints:
            logger.warning(f"Missing required budget constraint field: {field}")
            return False
    
    # Validate max_monthly_spend
    max_spend = constraints.get('max_monthly_spend')
    if not isinstance(max_spend, (int, float)) or max_spend <= 0:
        logger.warning("Invalid max_monthly_spend value")
        return False
    
    # Validate currency
    currency = constraints.get('currency')
    if not isinstance(currency, str) or len(currency) != 3:
        logger.warning("Invalid currency code")
        return False
    
    return True


def validate_recommendation_request(request: Dict[str, Any]) -> List[str]:
    """Validate recommendation request and return list of errors"""
    errors = []
    
    # Validate service ID
    if not validate_service_id(request.get('service_id', '')):
        errors.append("Invalid service_id format")
    
    # Validate budget constraints if provided
    if 'budget_constraints' in request and not validate_budget_constraints(request['budget_constraints']):
        errors.append("Invalid budget_constraints")
    
    # Validate priority filter if provided
    priority_filter = request.get('priority_filter')
    if priority_filter is not None and not validate_priority(priority_filter):
        errors.append("Invalid priority_filter: must be between 1 and 5")
    
    return errors


def validate_simulation_request(request: Dict[str, Any]) -> List[str]:
    """Validate simulation request and return list of errors"""
    errors = []
    
    # Validate service ID
    if not validate_service_id(request.get('service_id', '')):
        errors.append("Invalid service_id format")
    
    # Validate scenarios
    scenarios = request.get('scenarios', [])
    if not scenarios:
        errors.append("At least one scenario is required")
    
    for i, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"Scenario {i} must be an object")
            continue
            
        if 'name' not in scenario or not scenario['name']:
            errors.append(f"Scenario {i} must have a name")
            
        if 'changes' not in scenario or not isinstance(scenario['changes'], dict):
            errors.append(f"Scenario {i} must have changes object")
    
    # Validate duration
    duration = request.get('duration_hours', 24)
    if not isinstance(duration, int) or duration <= 0 or duration > 720:  # Max 30 days
        errors.append("duration_hours must be between 1 and 720")
    
    return errors


def validate_config_apply_request(request: Dict[str, Any]) -> List[str]:
    """Validate config apply request and return list of errors"""
    errors = []
    
    # Validate service ID
    if not validate_service_id(request.get('service_id', '')):
        errors.append("Invalid service_id format")
    
    # Validate recommendation ID
    if not validate_service_id(request.get('recommendation_id', '')):
        errors.append("Invalid recommendation_id format")
    
    return errors