from typing import Generator

from ..db.session import SessionLocal


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