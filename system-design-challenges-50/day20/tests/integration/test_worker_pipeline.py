import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.workers.tasks.recompute_costs import (
    recompute_service_costs, 
    generate_cost_report, 
    check_budget_alerts
)
from app.workers.tasks.pull_metrics import (
    pull_service_metrics, 
    analyze_service_performance, 
    generate_performance_report
)


class TestWorkerPipeline:
    """Integration tests for worker pipeline"""
    
    @pytest.mark.celery
    def test_recompute_service_costs_task(self):
        """Test recompute_service_costs Celery task"""
        # Mock the billing service
        with patch('app.workers.tasks.recompute_costs.BillingConnectorService') as mock_billing:
            mock_instance = mock_billing.return_value
            mock_instance.get_service_costs.return_value = {
                "total_cost": 1250.75,
                "cost_breakdown": {
                    "compute": 800.50,
                    "storage": 200.25,
                    "network": 150.00,
                    "other": 100.00
                }
            }
            
            # Mock database session
            with patch('app.workers.tasks.recompute_costs.get_db_session') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                mock_service_repo = MagicMock()
                with patch('app.workers.tasks.recompute_costs.ServiceRepository', return_value=mock_service_repo):
                    mock_service_repo.list_all.return_value = [
                        MagicMock(id="service_1", name="test-service-1"),
                        MagicMock(id="service_2", name="test-service-2")
                    ]
                    
                    # Run task
                    result = recompute_service_costs.delay()
                    
                    # Check result
                    assert result is not None
                    assert result.state != 'FAILURE'
    
    @pytest.mark.celery
    def test_generate_cost_report_task(self):
        """Test generate_cost_report Celery task"""
        # Mock the billing service
        with patch('app.workers.tasks.recompute_costs.BillingConnectorService') as mock_billing:
            mock_instance = mock_billing.return_value
            mock_instance.get_service_costs.return_value = {
                "total_cost": 1250.75
            }
            mock_instance.get_budget_status.return_value = {
                "budget_amount": 2000.00,
                "spent_amount": 1250.75
            }
            mock_instance.get_reserved_instance_utilization.return_value = {
                "total_savings": 750.00
            }
            mock_instance.get_cost_anomalies.return_value = []
            
            # Run task for specific service
            result = generate_cost_report.delay("service_123")
            
            # Check result
            assert result is not None
            assert result.state != 'FAILURE'
    
    @pytest.mark.celery
    def test_check_budget_alerts_task(self):
        """Test check_budget_alerts Celery task"""
        # Mock the billing service
        with patch('app.workers.tasks.recompute_costs.BillingConnectorService') as mock_billing:
            mock_instance = mock_billing.return_value
            mock_instance.get_budget_status.return_value = {
                "percentage_used": 62.5,
                "budget_amount": 2000.00,
                "spent_amount": 1250.75,
                "remaining_amount": 749.25
            }
            
            # Mock database session
            with patch('app.workers.tasks.recompute_costs.get_db_session') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                mock_service_repo = MagicMock()
                with patch('app.workers.tasks.recompute_costs.ServiceRepository', return_value=mock_service_repo):
                    mock_service_repo.list_all.return_value = [
                        MagicMock(id="service_1", name="test-service-1"),
                        MagicMock(id="service_2", name="test-service-2")
                    ]
                    
                    # Run task
                    result = check_budget_alerts.delay()
                    
                    # Check result
                    assert result is not None
                    assert result.state != 'FAILURE'
    
    @pytest.mark.celery
    def test_pull_service_metrics_task(self):
        """Test pull_service_metrics Celery task"""
        # Mock the telemetry service
        with patch('app.workers.tasks.pull_metrics.TelemetryConnectorService') as mock_telemetry:
            mock_instance = mock_telemetry.return_value
            mock_instance.get_performance_metrics.return_value = {
                "metrics": {
                    "latency": {"p95": 120},
                    "error_rate": {"percentage": 0.2}
                }
            }
            mock_instance.get_resource_utilization.return_value = {
                "resources": {
                    "cpu": {"utilization": 45.5},
                    "memory": {"utilization": 60.2}
                }
            }
            mock_instance.get_alerts.return_value = []
            
            # Mock database session
            with patch('app.workers.tasks.pull_metrics.get_db_session') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                mock_service_repo = MagicMock()
                with patch('app.workers.tasks.pull_metrics.ServiceRepository', return_value=mock_service_repo):
                    mock_service_repo.list_all.return_value = [
                        MagicMock(id="service_1", name="test-service-1"),
                        MagicMock(id="service_2", name="test-service-2")
                    ]
                    
                    # Run task
                    result = pull_service_metrics.delay()
                    
                    # Check result
                    assert result is not None
                    assert result.state != 'FAILURE'
    
    @pytest.mark.celery
    def test_analyze_service_performance_task(self):
        """Test analyze_service_performance Celery task"""
        # Mock the telemetry service
        with patch('app.workers.tasks.pull_metrics.TelemetryConnectorService') as mock_telemetry:
            mock_instance = mock_telemetry.return_value
            mock_instance.get_performance_metrics.return_value = {
                "metrics": {
                    "latency": {"p95": 120},
                    "error_rate": {"percentage": 0.2}
                }
            }
            mock_instance.get_resource_utilization.return_value = {
                "resources": {
                    "cpu": {"utilization": 45.5},
                    "memory": {"utilization": 60.2}
                }
            }
            
            # Mock database session
            with patch('app.workers.tasks.pull_metrics.get_db_session') as mock_session:
                mock_db = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_db
                
                mock_service_repo = MagicMock()
                with patch('app.workers.tasks.pull_metrics.ServiceRepository', return_value=mock_service_repo):
                    mock_service_repo.list_all.return_value = [
                        MagicMock(id="service_1", name="test-service-1"),
                        MagicMock(id="service_2", name="test-service-2")
                    ]
                    
                    # Run task
                    result = analyze_service_performance.delay()
                    
                    # Check result
                    assert result is not None
                    assert result.state != 'FAILURE'
    
    @pytest.mark.celery
    def test_generate_performance_report_task(self):
        """Test generate_performance_report Celery task"""
        # Mock the telemetry service
        with patch('app.workers.tasks.pull_metrics.TelemetryConnectorService') as mock_telemetry:
            mock_instance = mock_telemetry.return_value
            mock_instance.list_services.return_value = ["service_1", "service_2"]
            mock_instance.get_service_health.return_value = "healthy"
            mock_instance.get_performance_metrics.return_value = {
                "metrics": {
                    "latency": {"p95": 120},
                    "error_rate": {"percentage": 0.2}
                }
            }
            
            # Run task
            result = generate_performance_report.delay()
            
            # Check result
            assert result is not None
            assert result.state != 'FAILURE'