import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from app.db.session import get_db_session
from app.db.models import Recommendation, Service, ConfigChange, RecommendationStatus
from app.db.repositories.recommendation_repo import RecommendationRepository, ServiceRepository, ConfigChangeRepository
from app.schemas.recommendation import Recommendation as RecommendationSchema

# Set up logging
logger = logging.getLogger(__name__)


class CostModelService:
    """Service for cost optimization modeling and recommendations"""
    
    async def get_current_usage(self, service_id: str) -> Dict[str, Any]:
        """Get current resource usage for a service"""
        # In a real implementation, this would query telemetry data
        # For now, we'll return mock data
        return {
            "cpu_utilization": 45.5,
            "memory_utilization": 60.2,
            "disk_usage": 250.0,  # GB
            "network_in": 1000.0,  # Mbps
            "network_out": 500.0,  # Mbps
            "requests_per_second": 1500,
            "error_rate": 0.02,
            "latency_p95": 150,  # ms
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def generate_recommendations(
        self, 
        service_id: str, 
        current_usage: Dict[str, Any], 
        budget_constraints: Optional[Dict[str, Any]] = None
    ) -> List[RecommendationSchema]:
        """Generate cost optimization recommendations"""
        try:
            recommendations = []
            
            # CPU optimization recommendation
            if current_usage.get("cpu_utilization", 0) < 30:
                recommendations.append(RecommendationSchema(
                    id="rec_cpu_1",
                    service_id=service_id,
                    title="Downsize CPU Resources",
                    description=f"CPU utilization is only {current_usage.get('cpu_utilization', 0):.1f}%. Consider downsizing to reduce costs.",
                    estimated_savings=200.0,
                    implementation_cost=50.0,
                    priority=3,
                    config_changes=json.dumps({
                        "resource_type": "cpu",
                        "current": "4_cores",
                        "recommended": "2_cores"
                    }),
                    sla_impact=json.dumps({
                        "performance_impact": "minimal",
                        "risk_level": "low"
                    })
                ))
            
            # Memory optimization recommendation
            if current_usage.get("memory_utilization", 0) < 40:
                recommendations.append(RecommendationSchema(
                    id="rec_mem_1",
                    service_id=service_id,
                    title="Reduce Memory Allocation",
                    description=f"Memory utilization is only {current_usage.get('memory_utilization', 0):.1f}%. Consider reducing memory allocation.",
                    estimated_savings=150.0,
                    implementation_cost=25.0,
                    priority=2,
                    config_changes=json.dumps({
                        "resource_type": "memory",
                        "current": "8GB",
                        "recommended": "4GB"
                    }),
                    sla_impact=json.dumps({
                        "performance_impact": "minimal",
                        "risk_level": "low"
                    })
                ))
            
            # Storage optimization recommendation
            if current_usage.get("disk_usage", 0) < 500:
                recommendations.append(RecommendationSchema(
                    id="rec_disk_1",
                    service_id=service_id,
                    title="Optimize Storage Configuration",
                    description="Consider switching to more cost-effective storage options.",
                    estimated_savings=100.0,
                    implementation_cost=75.0,
                    priority=1,
                    config_changes=json.dumps({
                        "resource_type": "storage",
                        "current": "SSD_1TB",
                        "recommended": "Hybrid_SSD_HDD"
                    }),
                    sla_impact=json.dumps({
                        "performance_impact": "moderate",
                        "risk_level": "medium"
                    })
                ))
            
            # Save recommendations to database
            with get_db_session() as db:
                repo = RecommendationRepository(db)
                for rec in recommendations:
                    db_rec = Recommendation(
                        service_id=rec.service_id,
                        title=rec.title,
                        description=rec.description,
                        estimated_savings=rec.estimated_savings,
                        implementation_cost=rec.implementation_cost,
                        priority=rec.priority,
                        config_changes=rec.config_changes,
                        sla_impact=rec.sla_impact
                    )
                    repo.create(db_rec)
            
            logger.info(f"Generated {len(recommendations)} recommendations for service {service_id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise
    
    async def get_historical_recommendations(
        self, 
        service_id: str, 
        limit: int = 10
    ) -> List[RecommendationSchema]:
        """Get historical recommendations for a service"""
        try:
            with get_db_session() as db:
                repo = RecommendationRepository(db)
                db_recommendations = repo.get_historical(service_id, limit)
                
                # Convert to schema objects
                recommendations = []
                for db_rec in db_recommendations:
                    recommendations.append(RecommendationSchema(
                        id=db_rec.id,
                        service_id=db_rec.service_id,
                        title=db_rec.title,
                        description=db_rec.description,
                        estimated_savings=db_rec.estimated_savings,
                        implementation_cost=db_rec.implementation_cost,
                        priority=db_rec.priority,
                        status=db_rec.status,
                        config_changes=db_rec.config_changes,
                        sla_impact=db_rec.sla_impact,
                        created_at=db_rec.created_at,
                        updated_at=db_rec.updated_at
                    ))
                
                return recommendations
                
        except Exception as e:
            logger.error(f"Error fetching historical recommendations: {e}")
            raise
    
    async def apply_recommendation(
        self, 
        service_id: str, 
        recommendation_id: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Apply a cost optimization recommendation"""
        try:
            # In a real implementation, this would apply the actual configuration changes
            # For now, we'll simulate the application
            
            # Get recommendation from database
            with get_db_session() as db:
                rec_repo = RecommendationRepository(db)
                recommendation = rec_repo.get(recommendation_id)
                
                if not recommendation:
                    raise ValueError(f"Recommendation {recommendation_id} not found")
                
                # Update recommendation status
                rec_repo.update_status(recommendation_id, RecommendationStatus.APPLIED)
                
                # Create config change record
                config_repo = ConfigChangeRepository(db)
                config_change = ConfigChange(
                    service_id=service_id,
                    recommendation_id=recommendation_id,
                    change_type="cost_optimization",
                    old_config=json.dumps({"status": "before_change"}),
                    new_config=json.dumps({"status": "after_change", "parameters": parameters}),
                    applied_by="system"
                )
                config_repo.create(config_change)
            
            result = {
                "status": "success",
                "message": f"Recommendation {recommendation_id} applied successfully",
                "config_change_id": config_change.id,
                "applied_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Applied recommendation {recommendation_id} for service {service_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error applying recommendation: {e}")
            raise
    
    async def rollback_recommendation(
        self, 
        service_id: str, 
        recommendation_id: str
    ) -> Dict[str, Any]:
        """Rollback a previously applied recommendation"""
        try:
            # In a real implementation, this would rollback the configuration changes
            # For now, we'll simulate the rollback
            
            with get_db_session() as db:
                # Find config change associated with this recommendation
                config_repo = ConfigChangeRepository(db)
                # In a real implementation, we would find the specific config change
                # For now, we'll just mark it as rolled back
                
                # Update recommendation status
                rec_repo = RecommendationRepository(db)
                rec_repo.update_status(recommendation_id, RecommendationStatus.ROLLED_BACK)
                
                # Create rollback config change record
                rollback_change = ConfigChange(
                    service_id=service_id,
                    recommendation_id=recommendation_id,
                    change_type="rollback",
                    old_config=json.dumps({"status": "before_rollback"}),
                    new_config=json.dumps({"status": "after_rollback"}),
                    applied_by="system"
                )
                config_repo.create(rollback_change)
                
                # Mark original config change as rolled back
                # This would require finding the original config change
                
            result = {
                "status": "success",
                "message": f"Recommendation {recommendation_id} rolled back successfully",
                "rollback_change_id": rollback_change.id,
                "rolled_back_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Rolled back recommendation {recommendation_id} for service {service_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error rolling back recommendation: {e}")
            raise
    
    async def get_config_history(
        self, 
        service_id: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get configuration change history for a service"""
        try:
            with get_db_session() as db:
                config_repo = ConfigChangeRepository(db)
                db_changes = config_repo.get_history(service_id, limit)
                
                # Convert to dict objects
                changes = []
                for db_change in db_changes:
                    changes.append({
                        "id": db_change.id,
                        "service_id": db_change.service_id,
                        "recommendation_id": db_change.recommendation_id,
                        "change_type": db_change.change_type,
                        "applied_by": db_change.applied_by,
                        "applied_at": db_change.applied_at,
                        "rolled_back": db_change.rolled_back,
                        "rolled_back_at": db_change.rolled_back_at
                    })
                
                return changes
                
        except Exception as e:
            logger.error(f"Error fetching config history: {e}")
            raise