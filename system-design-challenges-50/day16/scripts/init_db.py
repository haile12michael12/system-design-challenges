import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.models.user import User
from app.db.models.token import Token

def init_db():
    """Initialize the database."""
    # Get database URL from environment or use default
    database_url = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
    
    # Create engine and session
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()