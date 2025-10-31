from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime, timedelta
from .models import Analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

# In-memory storage for analytics data (in production, this would be in a database)
analytics_data: Dict[int, Analytics] = {}

@router.get("/{question_id}")
async def get_question_analytics(question_id: int) -> Analytics:
    """Get analytics for a specific question"""
    if question_id not in analytics_data:
        raise HTTPException(status_code=404, detail="Analytics not found for this question")
    return analytics_data[question_id]

@router.get("/")
async def get_all_analytics() -> List[Analytics]:
    """Get analytics for all questions"""
    return list(analytics_data.values())

@router.post("/track-view/{question_id}")
async def track_view(question_id: int) -> Dict[str, str]:
    """Track a view for a question"""
    if question_id not in analytics_data:
        analytics_data[question_id] = Analytics(
            question_id=question_id,
            views=1,
            avg_rating=0.0,
            total_feedback=0
        )
    else:
        analytics_data[question_id].views += 1
        analytics_data[question_id].last_updated = datetime.utcnow()
    
    return {"message": "View tracked successfully"}

@router.post("/track-feedback/{question_id}")
async def track_feedback(question_id: int, rating: int) -> Dict[str, str]:
    """Track feedback for a question"""
    if question_id not in analytics_data:
        analytics_data[question_id] = Analytics(
            question_id=question_id,
            views=0,
            avg_rating=float(rating),
            total_feedback=1
        )
    else:
        # Update average rating
        current = analytics_data[question_id]
        total_rating = current.avg_rating * current.total_feedback + rating
        current.total_feedback += 1
        current.avg_rating = total_rating / current.total_feedback
        current.last_updated = datetime.utcnow()
    
    return {"message": "Feedback tracked successfully"}