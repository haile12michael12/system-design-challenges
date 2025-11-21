from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def setup_tracing(service_name: str):
    # Create a tracer provider
    tracer_provider = TracerProvider()
    
    # Create an OTLP exporter
    exporter = OTLPSpanExporter()
    
    # Add the exporter to the tracer provider
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    
    # Set the tracer provider as the global provider
    trace.set_tracer_provider(tracer_provider)
    
    # Get a tracer for the service
    tracer = trace.get_tracer(service_name)
    
    return tracer