from prometheus_client import Counter, Histogram, Gauge, Summary
from app.core.logging_config import get_logger

logger = get_logger("metrics_service")

# Define metrics
LOGS_INGESTED_TOTAL = Counter('logs_ingested_total', 'Total number of logs ingested', ['service', 'level'])
LOGS_INGESTION_DURATION = Histogram('logs_ingestion_duration_seconds', 'Time spent ingesting logs')
LOGS_QUERY_DURATION = Summary('logs_query_duration_seconds', 'Time spent querying logs')
LOGS_QUEUE_LENGTH = Gauge('logs_queue_length', 'Current length of the logs queue')
LOGS_BATCH_SIZE = Histogram('logs_batch_size', 'Size of log batches processed')

class MetricsService:
    @staticmethod
    def record_log_ingestion(service: str, level: str):
        """
        Record a log ingestion event
        """
        try:
            LOGS_INGESTED_TOTAL.labels(service=service, level=level).inc()
            logger.debug(f"Recorded log ingestion: service={service}, level={level}")
        except Exception as e:
            logger.error(f"Failed to record log ingestion: {str(e)}")
            
    @staticmethod
    def record_ingestion_duration(duration: float):
        """
        Record the duration of a log ingestion operation
        """
        try:
            LOGS_INGESTION_DURATION.observe(duration)
            logger.debug(f"Recorded ingestion duration: {duration}s")
        except Exception as e:
            logger.error(f"Failed to record ingestion duration: {str(e)}")
            
    @staticmethod
    def record_query_duration(duration: float):
        """
        Record the duration of a log query operation
        """
        try:
            LOGS_QUERY_DURATION.observe(duration)
            logger.debug(f"Recorded query duration: {duration}s")
        except Exception as e:
            logger.error(f"Failed to record query duration: {str(e)}")
            
    @staticmethod
    def set_queue_length(length: int):
        """
        Set the current queue length
        """
        try:
            LOGS_QUEUE_LENGTH.set(length)
            logger.debug(f"Set queue length: {length}")
        except Exception as e:
            logger.error(f"Failed to set queue length: {str(e)}")
            
    @staticmethod
    def record_batch_size(size: int):
        """
        Record the size of a log batch
        """
        try:
            LOGS_BATCH_SIZE.observe(size)
            logger.debug(f"Recorded batch size: {size}")
        except Exception as e:
            logger.error(f"Failed to record batch size: {str(e)}")