"""
Pytest Fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import AsyncSessionLocal

@pytest.fixture(scope="session")
def test_db():
    """Create a test database"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    """Create a test client"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    with TestClient(app) as c:
        yield c