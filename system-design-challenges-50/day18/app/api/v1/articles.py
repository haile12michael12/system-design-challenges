from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from ...services.news_service import NewsService
from ...services.prefetch_service import PrefetchService
from ...core.logging import logger

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/")
async def get_articles(
    category: Optional[str] = Query(None, description="Filter articles by category"),
    limit: int = Query(10, ge=1, le=100, description="Number of articles to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    prefetch: bool = Query(False, description="Enable prefetching for better performance")
) -> List[dict]:
    """
    Get articles with optional filtering and prefetching.
    
    Args:
        category: Filter articles by category
        limit: Number of articles to return
        offset: Offset for pagination
        prefetch: Enable prefetching for better performance
        
    Returns:
        List[dict]: List of articles
    """
    try:
        if prefetch:
            prefetch_service = PrefetchService()
            articles = await prefetch_service.get_prefetched_articles(category, limit, offset)
        else:
            news_service = NewsService()
            articles = await news_service.get_articles(category, limit, offset)
        
        logger.info(f"Retrieved {len(articles)} articles")
        return articles
    except Exception as e:
        logger.error(f"Error retrieving articles: {e}")
        return []


@router.get("/{article_id}")
async def get_article(article_id: int) -> dict:
    """
    Get a specific article by ID.
    
    Args:
        article_id: Article ID
        
    Returns:
        dict: Article data
    """
    try:
        news_service = NewsService()
        article = await news_service.get_article(article_id)
        
        if article:
            logger.info(f"Retrieved article {article_id}")
            return article
        else:
            logger.warning(f"Article {article_id} not found")
            return {"error": "Article not found"}
    except Exception as e:
        logger.error(f"Error retrieving article {article_id}: {e}")
        return {"error": "Internal server error"}