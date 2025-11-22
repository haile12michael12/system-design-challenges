from celery import shared_task
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

from app.workers.celery_app import celery_app
from app.services.telemetry_connector import TelemetryConnectorService
from app.db.session import get_db_session
from app.db.models import Service
from app.db.repositories.recommendation_repo import ServiceRepository

# Set up logging
logger = logging.getLogger(__name__)


@shared_task(bind=True, name="pull_service_metrics")
def pull_service_metrics(self, service_id: str = None) -> Dict[str, Any]:
    """Pull metrics for a specific service or all services"""
    try:
        logger.info(f"Starting metrics pull for service: {service_id or 'all'}")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        # Calculate time range (last hour)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        results = []
        
        if service_id:
            # Pull metrics for specific service
            metrics = telemetry_service.get_performance_metrics(service_id)
            resource_util = telemetry_service.get_resource_utilization(service_id)
            alerts = telemetry_service.get_alerts(service_id)
            
            results.append({
                "service_id": service_id,
                "metrics": metrics,
                "resource_utilization": resource_util,
                "alerts": alerts,
                "pulled_at": datetime.utcnow().isoformat()
            })
        else:
            # Pull metrics for all services
            with get_db_session() as db:
                service_repo = ServiceRepository(db)
                services = service_repo.list_all()
                
                for service in services:
                    try:
                        metrics = telemetry_service.get_performance_metrics(service.id)
                        resource_util = telemetry_service.get_resource_utilization(service.id)
                        alerts = telemetry_service.get_alerts(service.id)
                        
                        results.append({
                            "service_id": service.id,
                            "metrics": metrics,
                            "resource_utilization": resource_util,
                            "alerts": alerts,
                            "pulled_at": datetime.utcnow().isoformat()
                        })
                        logger.info(f"Pulled metrics for service {service.id}")
                    except Exception as e:
                        logger.error(f"Error pulling metrics for service {service.id}: {e}")
                        results.append({
                            "service_id": service.id,
                            "error": str(e),
                            "pulled_at": datetime.utcnow().isoformat()
                        })
        
        logger.info(f"Completed metrics pull for {len(results)} services")
        return {
            "status": "success",
            "results": results,
            "completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in metrics pull task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)


@shared_task(bind=True, name="analyze_service_performance")
def analyze_service_performance(self, service_id: str = None) -> Dict[str, Any]:
    """Analyze performance metrics for a service"""
    try:
        logger.info(f"Analyzing performance for service: {service_id or 'all'}")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        analysis_results = []
        
        if service_id:
            # Analyze performance for specific service
            metrics = telemetry_service.get_performance_metrics(service_id)
            resource_util = telemetry_service.get_resource_utilization(service_id)
            
            # Perform analysis
            analysis = _perform_performance_analysis(metrics, resource_util)
            
            analysis_results.append({
                "service_id": service_id,
                "analysis": analysis,
                "analyzed_at": datetime.utcnow().isoformat()
            })
        else:
            # Analyze performance for all services
            with get_db_session() as db:
                service_repo = ServiceRepository(db)
                services = service_repo.list_all()
                
                for service in services:
                    try:
                        metrics = telemetry_service.get_performance_metrics(service.id)
                        resource_util = telemetry_service.get_resource_utilization(service.id)
                        
                        # Perform analysis
                        analysis = _perform_performance_analysis(metrics, resource_util)
                        
                        analysis_results.append({
                            "service_id": service.id,
                            "analysis": analysis,
                            "analyzed_at": datetime.utcnow().isoformat()
                        })
                        logger.info(f"Analyzed performance for service {service.id}")
                    except Exception as e:
                        logger.error(f"Error analyzing performance for service {service.id}: {e}")
                        analysis_results.append({
                            "service_id": service.id,
                            "error": str(e),
                            "analyzed_at": datetime.utcnow().isoformat()
                        })
        
        logger.info(f"Completed performance analysis for {len(analysis_results)} services")
        return {
            "status": "success",
            "results": analysis_results,
            "completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in performance analysis task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)


def _perform_performance_analysis(metrics: Dict[str, Any], resource_util: Dict[str, Any]) -> Dict[str, Any]:
    """Perform detailed performance analysis"""
    analysis = {
        "recommendations": [],
        "issues": [],
        "health_score": 100
    }
    
    # Analyze latency
    latency_p95 = metrics.get("metrics", {}).get("latency", {}).get("p95", 0)
    if latency_p95 > 200:
        analysis["issues"].append({
            "type": "high_latency",
            "severity": "critical",
            "description": f"95th percentile latency is {latency_p95}ms, exceeding threshold of 200ms"
        })
        analysis["health_score"] -= 20
    elif latency_p95 > 150:
        analysis["issues"].append({
            "type": "moderate_latency",
            "severity": "warning",
            "description": f"95th percentile latency is {latency_p95}ms, approaching threshold"
        })
        analysis["health_score"] -= 10
    
    # Analyze error rate
    error_rate = metrics.get("metrics", {}).get("error_rate", {}).get("percentage", 0)
    if error_rate > 1.0:
        analysis["issues"].append({
            "type": "high_error_rate",
            "severity": "critical",
            "description": f"Error rate is {error_rate}%, exceeding threshold of 1%"
        })
        analysis["health_score"] -= 25
    elif error_rate > 0.5:
        analysis["issues"].append({
            "type": "moderate_error_rate",
            "severity": "warning",
            "description": f"Error rate is {error_rate}%, approaching threshold"
        })
        analysis["health_score"] -= 15
    
    # Analyze CPU utilization
    cpu_util = resource_util.get("resources", {}).get("cpu", {}).get("utilization", 0)
    if cpu_util > 85:
        analysis["issues"].append({
            "type": "high_cpu_utilization",
            "severity": "warning",
            "description": f"CPU utilization is {cpu_util}%, consider scaling"
        })
        analysis["health_score"] -= 10
    elif cpu_util < 15:
        analysis["recommendations"].append({
            "type": "cpu_optimization",
            "priority": "medium",
            "description": f"CPU utilization is only {cpu_util}%, consider rightsizing"
        })
    
    # Analyze memory utilization
    memory_util = resource_util.get("resources", {}).get("memory", {}).get("utilization", 0)
    if memory_util > 85:
        analysis["issues"].append({
            "type": "high_memory_utilization",
            "severity": "warning",
            "description": f"Memory utilization is {memory_util}%, consider scaling"
        })
        analysis["health_score"] -= 10
    elif memory_util < 20:
        analysis["recommendations"].append({
            "type": "memory_optimization",
            "priority": "medium",
            "description": f"Memory utilization is only {memory_util}%, consider rightsizing"
        })
    
    # Ensure health score doesn't go below 0
    analysis["health_score"] = max(0, analysis["health_score"])
    
    return analysis


@shared_task(bind=True, name="generate_performance_report")
def generate_performance_report(self) -> Dict[str, Any]:
    """Generate overall performance report"""
    try:
        logger.info("Generating overall performance report")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        # Get all services
        services = telemetry_service.list_services()
        
        report_data = {
            "services": [],
            "summary": {
                "total_services": len(services),
                "healthy_services": 0,
                "warning_services": 0,
                "critical_services": 0
            }
        }
        
        for service_id in services:
            try:
                health_status = telemetry_service.get_service_health(service_id)
                performance_metrics = telemetry_service.get_performance_metrics(service_id)
                
                service_data = {
                    "service_id": service_id,
                    "health_status": health_status,
                    "performance": performance_metrics
                }
                
                report_data["services"].append(service_data)
                
                # Update summary counts
                if health_status == "healthy":
                    report_data["summary"]["healthy_services"] += 1
                elif health_status == "warning":
                    report_data["summary"]["warning_services"] += 1
                else:
                    report_data["summary"]["critical_services"] += 1
                    
            except Exception as e:
                logger.error(f"Error generating report for service {service_id}: {e}")
        
        logger.info("Generated overall performance report")
        return {
            "status": "success",
            "report": report_data,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in performance report generation task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)