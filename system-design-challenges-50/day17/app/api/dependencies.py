from typing import Generator

from ..db.session import SessionLocal
from ..cache.redis_client import get_redis_client


def get_db() -> Generator:
    """
    Dependency to get a database session.
    
    Yields:
        SessionLocal: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> Generator:
    """
    Dependency to get a Redis client.
    
    Yields:
        Redis: Redis client
    """
    redis_client = get_redis_client()
    try:
        yield redis_client
    finally:
        pass  # Redis connections are typically pooled


def get_feed_writer_service():
    """
    Dependency to get a Feed Writer service instance.
    
    Returns:
        FeedWriterService: Feed writer service instance
    """
    from ..domain.services.feed_writer import FeedWriterService
    return FeedWriterService()


def get_feed_reader_service():
    """
    Dependency to get a Feed Reader service instance.
    
    Returns:
        FeedReaderService: Feed reader service instance
    """
    from ..domain.services.feed_reader import FeedReaderService
    return FeedReaderService()