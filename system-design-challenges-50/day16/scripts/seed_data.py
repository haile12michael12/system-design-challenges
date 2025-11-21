import os
import sys
from sqlalchemy.orm import sessionmaker
from app.db.session import engine
from app.db.base import Base
from app.db.models.user import User
from app.core.security import get_password_hash

def seed_data():
    """Seed the database with initial data."""
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_verified=True
        )
        
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if not existing_user:
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()