import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from app.main import app

client = TestClient(app)


class TestRecommendationAPI:
    """Unit tests for recommendation API endpoints"""
    
    def test_get_recommendations_success(self):
        """Test successful recommendation generation"""
        # Mock the services
        with patch('app.api.v1.recommend.recommendation_service') as mock_service:
            mock_service.get_current_usage.return_value = {
                "cpu_utilization": 45.5,
                "memory_utilization": 60.2
            }
            
            mock_service.generate_recommendations.return_value = [
                {
                    "id": "rec_1",
                    "service_id": "test-service-123",
                    "title": "Optimize CPU Resources",
                    "description": "Reduce CPU allocation to save costs",
                    "estimated_savings": 200.0,
                    "implementation_cost": 50.0,
                    "priority": 3
                }
            ]
            
            # Mock SLA engine
            with patch('app.api.v1.recommend.sla_engine') as mock_sla:
                mock_sla.validate_recommendations.return_value = [
                    {
                        "id": "rec_1",
                        "service_id": "test-service-123",
                        "title": "Optimize CPU Resources",
                        "description": "Reduce CPU allocation to save costs",
                        "estimated_savings": 200.0,
                        "implementation_cost": 50.0,
                        "priority": 3,
                        "sla_impact": '{"sla_compliant": true}'
                    }
                ]
                
                # Make request
                request_data = {
                    "service_id": "test-service-123",
                    "budget_constraints": {
                        "max_monthly_spend": 1000,
                        "currency": "USD"
                    }
                }
                
                response = client.post("/v1/recommend", json=request_data)
                
                assert response.status_code == 200
                data = response.json()
                assert "recommendations" in data
                assert len(data["recommendations"]) == 1
    
    def test_get_recommendations_validation_error(self):
        """Test recommendation generation with validation error"""
        # Make request with invalid data
        request_data = {
            "service_id": "",  # Invalid service ID
            "budget_constraints": {
                "max_monthly_spend": -100,  # Invalid spend
                "currency": "USD"
            }
        }
        
        response = client.post("/v1/recommend", json=request_data)
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_get_service_recommendations_success(self):
        """Test successful retrieval of historical recommendations"""
        # Mock the service
        with patch('app.api.v1.recommend.recommendation_service') as mock_service:
            mock_service.get_historical_recommendations.return_value = [
                {
                    "id": "rec_1",
                    "service_id": "test-service-123",
                    "title": "Optimize CPU Resources",
                    "description": "Reduce CPU allocation to save costs",
                    "estimated_savings": 200.0,
                    "implementation_cost": 50.0,
                    "priority": 3,
                    "status": "applied"
                }
            ]
            
            response = client.get("/v1/recommendations/test-service-123?limit=5")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
    
    def test_apply_recommendation_success(self):
        """Test successful recommendation application"""
        # Mock the service
        with patch('app.api.v1.config_apply.cost_model') as mock_service:
            mock_service.apply_recommendation.return_value = {
                "status": "success",
                "message": "Recommendation applied successfully",
                "result": {
                    "config_change_id": "change_123"
                }
            }
            
            # Make request
            request_data = {
                "service_id": "test-service-123",
                "recommendation_id": "rec_123",
                "parameters": {
                    "test": "value"
                }
            }
            
            response = client.post("/v1/config/apply", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "result" in data
    
    def test_rollback_recommendation_success(self):
        """Test successful recommendation rollback"""
        # Mock the service
        with patch('app.api.v1.config_apply.cost_model') as mock_service:
            mock_service.rollback_recommendation.return_value = {
                "status": "success",
                "message": "Recommendation rolled back successfully",
                "result": {
                    "rollback_change_id": "rollback_123"
                }
            }
            
            response = client.post("/v1/config/rollback/test-service-123/rec_123")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "result" in data
    
    def test_run_simulation_success(self):
        """Test successful simulation run"""
        # Mock the service
        with patch('app.api.v1.simulate.simulation_engine') as mock_service:
            mock_service.run_simulation.return_value = [
                {
                    "scenario": "cpu_optimization",
                    "description": "Optimize CPU resources",
                    "changes": {"cpu": -20},
                    "cost_before": 1000.0,
                    "cost_after": 800.0,
                    "estimated_savings": 200.0,
                    "performance_impact": -5.0,
                    "sla_compliance": True,
                    "duration_hours": 24
                }
            ]
            
            # Make request
            request_data = {
                "service_id": "test-service-123",
                "scenarios": [
                    {
                        "name": "cpu_optimization",
                        "description": "Optimize CPU resources",
                        "changes": {"cpu": -20}
                    }
                ],
                "duration_hours": 24
            }
            
            response = client.post("/v1/simulate", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "scenarios" in data
            assert len(data["scenarios"]) == 1
    
    def test_get_simulation_templates_success(self):
        """Test successful retrieval of simulation templates"""
        # Mock the service
        with patch('app.api.v1.simulate.simulation_engine') as mock_service:
            mock_service.get_templates.return_value = [
                "cpu_optimization",
                "memory_optimization",
                "storage_optimization"
            ]
            
            response = client.get("/v1/simulate/templates")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 3