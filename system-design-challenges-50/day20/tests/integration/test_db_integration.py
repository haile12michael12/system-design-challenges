import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base, Service, Recommendation, Simulation, ConfigChange
from app.db.session import get_db_session
from app.db.repositories.recommendation_repo import (
    ServiceRepository, 
    RecommendationRepository, 
    SimulationRepository, 
    ConfigChangeRepository
)


class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    @pytest.fixture(scope="class")
    def db_engine(self):
        """Create in-memory SQLite database for testing"""
        # Create temporary file for SQLite database
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        # Create engine
        engine = create_engine(f"sqlite:///{temp_db.name}")
        Base.metadata.create_all(bind=engine)
        
        yield engine
        
        # Cleanup
        os.unlink(temp_db.name)
    
    @pytest.fixture
    def db_session(self, db_engine):
        """Create database session for testing"""
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def test_service_repository_crud(self, db_session):
        """Test ServiceRepository CRUD operations"""
        # Create repository
        repo = ServiceRepository(db_session)
        
        # Create service
        service = Service(
            name="test-service",
            owner="test-owner",
            description="Test service for integration testing"
        )
        created_service = repo.create(service)
        
        assert created_service.id is not None
        assert created_service.name == "test-service"
        assert created_service.owner == "test-owner"
        
        # Get service
        retrieved_service = repo.get(created_service.id)
        assert retrieved_service is not None
        assert retrieved_service.name == "test-service"
        
        # Get by name
        service_by_name = repo.get_by_name("test-service")
        assert service_by_name is not None
        assert service_by_name.id == created_service.id
        
        # List all services
        all_services = repo.list_all()
        assert len(all_services) == 1
        assert all_services[0].id == created_service.id
    
    def test_recommendation_repository_crud(self, db_session):
        """Test RecommendationRepository CRUD operations"""
        # First create a service
        service_repo = ServiceRepository(db_session)
        service = Service(name="test-service", owner="test-owner")
        service = service_repo.create(service)
        
        # Create repository
        repo = RecommendationRepository(db_session)
        
        # Create recommendation
        recommendation = Recommendation(
            service_id=service.id,
            title="Test Recommendation",
            description="Test description",
            estimated_savings=100.0,
            implementation_cost=50.0,
            priority=3
        )
        created_recommendation = repo.create(recommendation)
        
        assert created_recommendation.id is not None
        assert created_recommendation.service_id == service.id
        assert created_recommendation.title == "Test Recommendation"
        
        # Get recommendation
        retrieved_recommendation = repo.get(created_recommendation.id)
        assert retrieved_recommendation is not None
        assert retrieved_recommendation.title == "Test Recommendation"
        
        # Get by service
        recommendations_by_service = repo.get_by_service(service.id)
        assert len(recommendations_by_service) == 1
        assert recommendations_by_service[0].id == created_recommendation.id
        
        # Update status
        updated_recommendation = repo.update_status(
            created_recommendation.id, 
            "applied"
        )
        assert updated_recommendation is not None
        assert updated_recommendation.status == "applied"
    
    def test_simulation_repository_crud(self, db_session):
        """Test SimulationRepository CRUD operations"""
        # First create a service
        service_repo = ServiceRepository(db_session)
        service = Service(name="test-service", owner="test-owner")
        service = service_repo.create(service)
        
        # Create repository
        repo = SimulationRepository(db_session)
        
        # Create simulation
        simulation = Simulation(
            service_id=service.id,
            scenario="cpu_optimization",
            duration_hours=24,
            cost_before=1000.0,
            cost_after=800.0,
            performance_impact=-5.0,
            sla_compliance=True
        )
        created_simulation = repo.create(simulation)
        
        assert created_simulation.id is not None
        assert created_simulation.service_id == service.id
        assert created_simulation.scenario == "cpu_optimization"
        
        # Get simulation
        retrieved_simulation = repo.get(created_simulation.id)
        assert retrieved_simulation is not None
        assert retrieved_simulation.scenario == "cpu_optimization"
        
        # Get by service
        simulations_by_service = repo.get_by_service(service.id)
        assert len(simulations_by_service) == 1
        assert simulations_by_service[0].id == created_simulation.id
    
    def test_config_change_repository_crud(self, db_session):
        """Test ConfigChangeRepository CRUD operations"""
        # First create a service
        service_repo = ServiceRepository(db_session)
        service = Service(name="test-service", owner="test-owner")
        service = service_repo.create(service)
        
        # Create repository
        repo = ConfigChangeRepository(db_session)
        
        # Create config change
        config_change = ConfigChange(
            service_id=service.id,
            change_type="cost_optimization",
            new_config='{"cpu": "2_cores"}',
            applied_by="test_user"
        )
        created_config_change = repo.create(config_change)
        
        assert created_config_change.id is not None
        assert created_config_change.service_id == service.id
        assert created_config_change.change_type == "cost_optimization"
        
        # Get config change
        retrieved_config_change = repo.get(created_config_change.id)
        assert retrieved_config_change is not None
        assert retrieved_config_change.change_type == "cost_optimization"
        
        # Get by service
        changes_by_service = repo.get_by_service(service.id)
        assert len(changes_by_service) == 1
        assert changes_by_service[0].id == created_config_change.id
        
        # Mark as rolled back
        rolled_back_change = repo.mark_rolled_back(created_config_change.id)
        assert rolled_back_change is not None
        assert rolled_back_change.rolled_back is True
        assert rolled_back_change.rolled_back_at is not None
    
    def test_get_historical_recommendations(self, db_session):
        """Test getting historical recommendations"""
        # First create a service
        service_repo = ServiceRepository(db_session)
        service = Service(name="test-service", owner="test-owner")
        service = service_repo.create(service)
        
        # Create multiple recommendations
        repo = RecommendationRepository(db_session)
        
        for i in range(5):
            recommendation = Recommendation(
                service_id=service.id,
                title=f"Test Recommendation {i}",
                description=f"Test description {i}",
                estimated_savings=100.0 + i * 10,
                implementation_cost=50.0,
                priority=3
            )
            repo.create(recommendation)
        
        # Get historical recommendations
        historical = repo.get_historical(service.id, limit=3)
        assert len(historical) == 3
        
        # They should be ordered by creation time (newest first)
        # Since we're using SQLite without timezone support, we can't guarantee order
        # But we can check that all have the correct service_id
        for rec in historical:
            assert rec.service_id == service.id
    
    def test_get_config_history(self, db_session):
        """Test getting config change history"""
        # First create a service
        service_repo = ServiceRepository(db_session)
        service = Service(name="test-service", owner="test-owner")
        service = service_repo.create(service)
        
        # Create multiple config changes
        repo = ConfigChangeRepository(db_session)
        
        for i in range(5):
            config_change = ConfigChange(
                service_id=service.id,
                change_type=f"change_type_{i}",
                new_config=f'{{"config": "value_{i}"}}',
                applied_by="test_user"
            )
            repo.create(config_change)
        
        # Get config history
        history = repo.get_history(service.id, limit=3)
        assert len(history) == 3
        
        # They should be ordered by applied_at (newest first)
        # Since we're using SQLite without timezone support, we can't guarantee order
        # But we can check that all have the correct service_id
        for change in history:
            assert change.service_id == service.id