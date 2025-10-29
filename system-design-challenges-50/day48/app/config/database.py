from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .settings import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_database():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables"""
    from ..models.data_lake import Base as DataLakeBase
    from ..models.ingestion import Base as IngestionBase
    from ..models.schema_evolution import Base as SchemaEvolutionBase
    
    # Create all tables
    DataLakeBase.metadata.create_all(bind=engine)
    IngestionBase.metadata.create_all(bind=engine)
    SchemaEvolutionBase.metadata.create_all(bind=engine)
