import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.services.sla_engine import SLAEngineService
from app.schemas.recommendation import Recommendation


class TestSLAEngineService:
    """Unit tests for SLAEngineService"""
    
    @pytest.fixture
    def sla_engine_service(self):
        """Fixture for SLAEngineService"""
        return SLAEngineService()
    
    @pytest.mark.asyncio
    async def test_validate_recommendations(self, sla_engine_service):
        """Test validate_recommendations method"""
        service_id = "test-service-123"
        recommendations = [
            Recommendation(
                id="rec_1",
                service_id=service_id,
                title="Test Recommendation",
                description="Test Description",
                estimated_savings=100.0,
                implementation_cost=50.0,
                priority=3
            )
        ]
        
        validated_recommendations = await sla_engine_service.validate_recommendations(
            service_id,
            recommendations
        )
        
        assert isinstance(validated_recommendations, list)
        assert len(validated_recommendations) == 1
        
        # Check that SLA impact was added
        rec = validated_recommendations[0]
        assert rec.sla_impact is not None
    
    @pytest.mark.asyncio
    async def test_monitor_sla_compliance(self, sla_engine_service):
        """Test monitor_sla_compliance method"""
        service_id = "test-service-123"
        recommendation_id = "rec_123"
        
        # Mock the SLA metrics
        with patch.object(sla_engine_service, '_get_sla_metrics') as mock_metrics:
            mock_metrics.return_value = {
                "availability": 99.95,
                "latency_p95": 120,
                "error_rate": 0.01
            }
            
            result = await sla_engine_service.monitor_sla_compliance(
                service_id,
                recommendation_id
            )
            
            assert result["service_id"] == service_id
            assert result["recommendation_id"] == recommendation_id
            assert "status" in result
            assert "metrics" in result
    
    @pytest.mark.asyncio
    async def test_generate_sla_report(self, sla_engine_service):
        """Test generate_sla_report method"""
        service_id = "test-service-123"
        time_range = "24h"
        
        # Mock the SLA metrics
        with patch.object(sla_engine_service, '_get_sla_metrics') as mock_metrics:
            mock_metrics.return_value = {
                "availability": 99.95,
                "latency_p95": 120,
                "error_rate": 0.01,
                "cpu_sla_threshold": 99.9,
                "memory_sla_threshold": 99.5
            }
            
            report = await sla_engine_service.generate_sla_report(
                service_id,
                time_range
            )
            
            assert report["service_id"] == service_id
            assert report["time_range"] == time_range
            assert "sla_summary" in report
            assert "recommendations" in report
            
            # Check SLA summary structure
            sla_summary = report["sla_summary"]
            assert "availability" in sla_summary
            assert "latency" in sla_summary
            assert "error_rate" in sla_summary
    
    @pytest.mark.asyncio
    async def test_check_sla_compliance(self, sla_engine_service):
        """Test _check_sla_compliance method"""
        service_id = "test-service-123"
        recommendation = Recommendation(
            id="rec_1",
            service_id=service_id,
            title="Test Recommendation",
            description="Test Description",
            estimated_savings=100.0,
            implementation_cost=50.0,
            priority=3,
            sla_impact='{"risk_level": "low"}'
        )
        
        # Mock the SLA metrics
        with patch.object(sla_engine_service, '_get_sla_metrics') as mock_metrics:
            mock_metrics.return_value = {
                "availability": 99.95,
                "latency_p95": 120,
                "error_rate": 0.01,
                "cpu_sla_threshold": 99.9,
                "memory_sla_threshold": 99.5
            }
            
            is_compliant = await sla_engine_service._check_sla_compliance(
                service_id,
                recommendation
            )
            
            assert isinstance(is_compliant, bool)
    
    @pytest.mark.asyncio
    async def test_get_sla_metrics(self, sla_engine_service):
        """Test _get_sla_metrics method"""
        service_id = "test-service-123"
        
        metrics = await sla_engine_service._get_sla_metrics(service_id)
        
        assert isinstance(metrics, dict)
        assert "availability" in metrics
        assert "latency_p95" in metrics
        assert "error_rate" in metrics
        assert "timestamp" in metrics