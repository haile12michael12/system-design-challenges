"""Database initialization"""
from app.db.base import Base
from app.db.session import engine

def init_db():
    """Initialize the database"""
    # Create all tables
    Base.metadata.create_all(bind=engine)

def drop_db():
    """Drop all tables"""
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")