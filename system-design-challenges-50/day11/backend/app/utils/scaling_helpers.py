def calculate_scaling_factor(current_capacity: int, required_capacity: int) -> float:
    """Calculate scaling factor based on current and required capacity"""
    if current_capacity == 0:
        return 1.0
    return required_capacity / current_capacity

def determine_scaling_type(workload_pattern: str) -> str:
    """Determine optimal scaling type based on workload pattern"""
    if workload_pattern == "spiky":
        return "horizontal"
    elif workload_pattern == "steady":
        return "vertical"
    else:
        return "hybrid"