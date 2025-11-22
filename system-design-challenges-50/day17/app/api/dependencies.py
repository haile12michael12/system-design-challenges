from typing import Generator
from sqlalchemy.orm import Session

# Import database session
from ..db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import repositories
from ..db.repositories.user_repo import UserRepository
from ..db.repositories.post_repo import PostRepository
from ..db.repositories.follower_repo import FollowerRepository


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency to get user repository."""
    return UserRepository(db)


def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    """Dependency to get post repository."""
    return PostRepository(db)


def get_follower_repository(db: Session = Depends(get_db)) -> FollowerRepository:
    """Dependency to get follower repository."""
    return FollowerRepository(db)


# Import services
from ..domain.services.feed_writer import FeedWriterService
from ..domain.services.feed_reader import FeedReaderService


def get_feed_writer_service(
    post_repo: PostRepository = Depends(get_post_repository),
    event_publisher = None  # Would import from message_bus in real implementation
) -> FeedWriterService:
    """Dependency to get feed writer service."""
    return FeedWriterService(post_repo, event_publisher)


def get_feed_reader_service(
    post_repo: PostRepository = Depends(get_post_repository),
    feed_cache = None  # Would import from cache in real implementation
) -> FeedReaderService:
    """Dependency to get feed reader service."""
    return FeedReaderService(post_repo, feed_cache)