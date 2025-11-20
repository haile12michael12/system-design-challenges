from ..db.models import ScalingDecision
import time

def get_scaling_recommendation(current_instances: int, workload: int) -> ScalingDecision:
    """Get autoscaling recommendation based on current instances and workload"""
    
    # Simple heuristic: if workload > instances * 10, scale up/out
    threshold = current_instances * 10
    
    if workload > threshold * 1.5:
        action = "scale_up" if current_instances <= 5 else "scale_out"
        new_instances = current_instances + (1 if action == "scale_up" else 2)
        reason = f"Workload ({workload}) significantly exceeds capacity ({threshold})"
    elif workload < threshold * 0.5:
        action = "scale_down" if current_instances > 1 else "scale_in"
        new_instances = max(1, current_instances - (1 if action == "scale_down" else 2))
        reason = f"Workload ({workload}) is significantly below capacity ({threshold})"
    else:
        action = "no_action"
        new_instances = current_instances
        reason = f"Workload ({workload}) is within acceptable range of capacity ({threshold})"
    
    return ScalingDecision(
        timestamp=time.time(),
        action=action,
        reason=reason,
        current_instances=current_instances,
        new_instances=new_instances
    )