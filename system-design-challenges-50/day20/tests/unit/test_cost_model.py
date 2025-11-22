import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.services.cost_model import CostModelService
from app.schemas.recommendation import Recommendation


class TestCostModelService:
    """Unit tests for CostModelService"""
    
    @pytest.fixture
    def cost_model_service(self):
        """Fixture for CostModelService"""
        return CostModelService()
    
    @pytest.mark.asyncio
    async def test_get_current_usage(self, cost_model_service):
        """Test get_current_usage method"""
        service_id = "test-service-123"
        
        # Mock the telemetry connector
        with patch('app.services.cost_model.TelemetryConnectorService') as mock_telemetry:
            mock_instance = mock_telemetry.return_value
            mock_instance.get_resource_utilization.return_value = {
                "cpu_utilization": 45.5,
                "memory_utilization": 60.2
            }
            
            usage = await cost_model_service.get_current_usage(service_id)
            
            assert "cpu_utilization" in usage
            assert "memory_utilization" in usage
            assert usage["cpu_utilization"] == 45.5
            assert usage["memory_utilization"] == 60.2
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, cost_model_service):
        """Test generate_recommendations method"""
        service_id = "test-service-123"
        current_usage = {
            "cpu_utilization": 25.0,
            "memory_utilization": 30.0,
            "disk_usage": 250.0
        }
        
        recommendations = await cost_model_service.generate_recommendations(
            service_id, 
            current_usage
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check that recommendations have expected fields
        for rec in recommendations:
            assert isinstance(rec, Recommendation)
            assert rec.service_id == service_id
            assert rec.title
            assert rec.description
            assert rec.estimated_savings >= 0
    
    @pytest.mark.asyncio
    async def test_get_historical_recommendations(self, cost_model_service):
        """Test get_historical_recommendations method"""
        service_id = "test-service-123"
        limit = 5
        
        # Mock database session
        with patch('app.services.cost_model.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            mock_repo = MagicMock()
            with patch('app.services.cost_model.RecommendationRepository', return_value=mock_repo):
                mock_repo.get_historical.return_value = [
                    MagicMock(
                        id="rec_1",
                        service_id=service_id,
                        title="Test Recommendation",
                        description="Test Description",
                        estimated_savings=100.0,
                        implementation_cost=50.0,
                        priority=3,
                        status="pending",
                        config_changes=None,
                        sla_impact=None,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                ]
                
                recommendations = await cost_model_service.get_historical_recommendations(
                    service_id, 
                    limit
                )
                
                assert isinstance(recommendations, list)
                assert len(recommendations) == 1
                assert recommendations[0].id == "rec_1"
    
    @pytest.mark.asyncio
    async def test_apply_recommendation(self, cost_model_service):
        """Test apply_recommendation method"""
        service_id = "test-service-123"
        recommendation_id = "rec_123"
        parameters = {"test": "value"}
        
        # Mock database session
        with patch('app.services.cost_model.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            mock_rec_repo = MagicMock()
            mock_config_repo = MagicMock()
            
            with patch('app.services.cost_model.RecommendationRepository', return_value=mock_rec_repo):
                with patch('app.services.cost_model.ConfigChangeRepository', return_value=mock_config_repo):
                    mock_rec_repo.get.return_value = MagicMock(id=recommendation_id)
                    mock_config_repo.create.return_value = MagicMock(id="config_change_123")
                    
                    result = await cost_model_service.apply_recommendation(
                        service_id,
                        recommendation_id,
                        parameters
                    )
                    
                    assert result["status"] == "success"
                    assert "config_change_id" in result
    
    @pytest.mark.asyncio
    async def test_rollback_recommendation(self, cost_model_service):
        """Test rollback_recommendation method"""
        service_id = "test-service-123"
        recommendation_id = "rec_123"
        
        # Mock database session
        with patch('app.services.cost_model.get_db_session') as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            
            mock_rec_repo = MagicMock()
            mock_config_repo = MagicMock()
            
            with patch('app.services.cost_model.RecommendationRepository', return_value=mock_rec_repo):
                with patch('app.services.cost_model.ConfigChangeRepository', return_value=mock_config_repo):
                    mock_config_repo.create.return_value = MagicMock(id="rollback_change_123")
                    
                    result = await cost_model_service.rollback_recommendation(
                        service_id,
                        recommendation_id
                    )
                    
                    assert result["status"] == "success"
                    assert "rollback_change_id" in result