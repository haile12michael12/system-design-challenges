from typing import Dict, List, Tuple, Optional
from .models import Question, Feedback, Analytics

def calculate_question_score(analytics: Optional[Analytics], feedbacks: List[Feedback]) -> float:
    """
    Calculate a score for a question based on analytics and feedback.
    
    Scoring factors:
    - Average rating (40% weight)
    - View count (30% weight)
    - Feedback volume (20% weight)
    - Recency factor (10% weight)
    
    Returns a score between 0 and 100.
    """
    if not analytics:
        return 0.0
    
    # Rating component (40% weight)
    rating_score = (analytics.avg_rating / 5.0) * 40.0 if analytics.avg_rating else 0.0
    
    # View count component (30% weight)
    # Normalize views to a 0-30 scale (assuming 1000+ views is excellent)
    view_score = min(analytics.views / 1000.0 * 30.0, 30.0)
    
    # Feedback volume component (20% weight)
    # Normalize feedback count to a 0-20 scale (assuming 100+ feedback is excellent)
    feedback_score = min(analytics.total_feedback / 100.0 * 20.0, 20.0)
    
    # Recency factor (10% weight)
    # New questions get a small bonus
    recency_score = 5.0  # Simplified - in practice, this would be calculated based on dates
    
    total_score = rating_score + view_score + feedback_score + recency_score
    return min(total_score, 100.0)  # Cap at 100

def rank_questions(questions: List[Question], 
                  analytics_data: Dict[int, Analytics], 
                  feedback_data: Dict[int, List[Feedback]]) -> List[Tuple[Question, float]]:
    """
    Rank questions by their calculated scores.
    
    Returns a list of (question, score) tuples sorted by score descending.
    """
    scored_questions = []
    
    for question in questions:
        q_id = question.id
        if q_id is not None:
            analytics = analytics_data.get(q_id)
            feedbacks = feedback_data.get(q_id, [])
            score = calculate_question_score(analytics, feedbacks)
            scored_questions.append((question, score))
    
    # Sort by score descending
    scored_questions.sort(key=lambda x: x[1], reverse=True)
    return scored_questions

def get_top_questions(questions: List[Question], 
                     analytics_data: Dict[int, Analytics], 
                     feedback_data: Dict[int, List[Feedback]], 
                     limit: int = 10) -> List[Tuple[Question, float]]:
    """
    Get the top N questions based on their scores.
    """
    ranked_questions = rank_questions(questions, analytics_data, feedback_data)
    return ranked_questions[:limit]