from celery import shared_task
from typing import Dict, Any
import logging
from datetime import datetime, timedelta

from app.workers.celery_app import celery_app
from app.services.billing_connector import BillingConnectorService
from app.db.session import get_db_session
from app.db.models import Service
from app.db.repositories.recommendation_repo import ServiceRepository

# Set up logging
logger = logging.getLogger(__name__)


@shared_task(bind=True, name="recompute_service_costs")
def recompute_service_costs(self, service_id: str = None) -> Dict[str, Any]:
    """Recompute costs for a specific service or all services"""
    try:
        logger.info(f"Starting cost recomputation for service: {service_id or 'all'}")
        
        # Initialize service
        billing_service = BillingConnectorService()
        
        # Calculate date range (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        results = []
        
        if service_id:
            # Recompute costs for specific service
            costs = billing_service.get_service_costs(
                service_id,
                start_date.isoformat(),
                end_date.isoformat()
            )
            results.append({
                "service_id": service_id,
                "costs": costs,
                "recomputed_at": datetime.utcnow().isoformat()
            })
        else:
            # Recompute costs for all services
            with get_db_session() as db:
                service_repo = ServiceRepository(db)
                services = service_repo.list_all()
                
                for service in services:
                    try:
                        costs = billing_service.get_service_costs(
                            service.id,
                            start_date.isoformat(),
                            end_date.isoformat()
                        )
                        results.append({
                            "service_id": service.id,
                            "costs": costs,
                            "recomputed_at": datetime.utcnow().isoformat()
                        })
                        logger.info(f"Recomputed costs for service {service.id}")
                    except Exception as e:
                        logger.error(f"Error recomputing costs for service {service.id}: {e}")
                        results.append({
                            "service_id": service.id,
                            "error": str(e),
                            "recomputed_at": datetime.utcnow().isoformat()
                        })
        
        logger.info(f"Completed cost recomputation for {len(results)} services")
        return {
            "status": "success",
            "results": results,
            "completed_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in cost recomputation task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)


@shared_task(bind=True, name="generate_cost_report")
def generate_cost_report(self, service_id: str = None) -> Dict[str, Any]:
    """Generate cost report for a service"""
    try:
        logger.info(f"Generating cost report for service: {service_id or 'all'}")
        
        # Initialize service
        billing_service = BillingConnectorService()
        
        # Calculate date range (last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        if service_id:
            # Generate report for specific service
            costs = billing_service.get_service_costs(
                service_id,
                start_date.isoformat(),
                end_date.isoformat()
            )
            
            budget_status = billing_service.get_budget_status(service_id)
            
            reserved_utilization = billing_service.get_reserved_instance_utilization(service_id)
            
            anomalies = billing_service.get_cost_anomalies(service_id, days=30)
            
            report = {
                "service_id": service_id,
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "costs": costs,
                "budget": budget_status,
                "reserved_instances": reserved_utilization,
                "anomalies": anomalies,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Generated cost report for service {service_id}")
            return {
                "status": "success",
                "report": report
            }
        else:
            # Generate reports for all services
            reports = []
            
            with get_db_session() as db:
                service_repo = ServiceRepository(db)
                services = service_repo.list_all()
                
                for service in services:
                    try:
                        report_task = generate_cost_report.delay(service.id)
                        reports.append({
                            "service_id": service.id,
                            "task_id": report_task.id
                        })
                    except Exception as e:
                        logger.error(f"Error generating report for service {service.id}: {e}")
                        reports.append({
                            "service_id": service.id,
                            "error": str(e)
                        })
            
            return {
                "status": "success",
                "reports": reports
            }
            
    except Exception as e:
        logger.error(f"Error in cost report generation task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)


@shared_task(bind=True, name="check_budget_alerts")
def check_budget_alerts(self) -> Dict[str, Any]:
    """Check budget alerts for all services"""
    try:
        logger.info("Checking budget alerts for all services")
        
        # Initialize service
        billing_service = BillingConnectorService()
        
        alerts = []
        
        with get_db_session() as db:
            service_repo = ServiceRepository(db)
            services = service_repo.list_all()
            
            for service in services:
                try:
                    budget_status = billing_service.get_budget_status(service.id)
                    
                    # Check if budget is exceeded or close to limit
                    percentage_used = budget_status.get("percentage_used", 0)
                    
                    if percentage_used >= 90:
                        alert_level = "critical" if percentage_used >= 95 else "warning"
                        
                        alerts.append({
                            "service_id": service.id,
                            "alert_level": alert_level,
                            "percentage_used": percentage_used,
                            "budget_amount": budget_status.get("budget_amount"),
                            "spent_amount": budget_status.get("spent_amount"),
                            "remaining_amount": budget_status.get("remaining_amount")
                        })
                        
                        logger.warning(f"Budget alert for service {service.id}: {percentage_used}% used")
                        
                except Exception as e:
                    logger.error(f"Error checking budget for service {service.id}: {e}")
        
        logger.info(f"Checked budget alerts for {len(services)} services, found {len(alerts)} alerts")
        return {
            "status": "success",
            "alerts": alerts,
            "checked_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in budget alert checking task: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)