class MetricsCollector:
    """Collect and process metrics for autoscaling decisions"""
    
    @staticmethod
    def calculate_average_latency(metrics_data):
        """Calculate average latency from metrics data"""
        if not metrics_data:
            return 0
        return sum(m.latency for m in metrics_data) / len(metrics_data)
    
    @staticmethod
    def calculate_total_cost(metrics_data):
        """Calculate total cost from metrics data"""
        return sum(m.cost for m in metrics_data)