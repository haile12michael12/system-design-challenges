class CostCalculator:
    """Calculate costs for different scaling strategies"""
    
    BASE_INSTANCE_COST = 0.1  # Cost per instance per unit time
    VERTICAL_SCALING_MULTIPLIER = 1.5  # Cost multiplier for vertical scaling
    HORIZONTAL_SCALING_MULTIPLIER = 1.2  # Cost multiplier for horizontal scaling
    
    @classmethod
    def calculate_vertical_scaling_cost(cls, instances: int, scaling_factor: float) -> float:
        """Calculate cost for vertical scaling"""
        return instances * cls.BASE_INSTANCE_COST * cls.VERTICAL_SCALING_MULTIPLIER * scaling_factor
    
    @classmethod
    def calculate_horizontal_scaling_cost(cls, instances: int, new_instances: int) -> float:
        """Calculate cost for horizontal scaling"""
        return (instances + new_instances) * cls.BASE_INSTANCE_COST * cls.HORIZONTAL_SCALING_MULTIPLIER