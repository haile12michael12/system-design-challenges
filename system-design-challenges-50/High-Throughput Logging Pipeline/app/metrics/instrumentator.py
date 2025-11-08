from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import CollectorRegistry

def setup_metrics(app):
    """
    Setup Prometheus metrics for the FastAPI application
    """
    # Create a custom registry
    registry = CollectorRegistry()
    
    # Create instrumentator
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        env_var_name="ENABLE_METRICS",
        registry=registry
    )
    
    # Add default metrics
    instrumentator.add(
        metrics.request_count(
            should_include_method=True,
            should_include_status=True,
            should_include_latency=True
        )
    ).add(
        metrics.requests_in_progress(
            should_include_method=True,
            should_include_status=True
        )
    ).add(
        metrics.latency(
            should_include_method=True,
            should_include_status=True
        )
    )
    
    # Instrument the app
    instrumentator.instrument(app)
    
    return instrumentator

def start_metrics_server():
    """
    Start the Prometheus metrics server
    """
    from prometheus_client import start_http_server
    start_http_server(8001)  # Start metrics server on port 8001