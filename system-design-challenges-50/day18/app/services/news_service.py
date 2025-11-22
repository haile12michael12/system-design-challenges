import json
from typing import List, Optional, Dict, Any
import asyncio
import time

from ..db.models import Article
from ..db.session import SessionLocal
from ..services.cache import get_cache_service
from ..core.config import settings
from ..core.logging import logger


class NewsService:
    """Service for handling news articles."""
    
    def __init__(self):
        self.cache_service = get_cache_service()
    
    async def get_articles(self, category: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get articles with optional filtering by category.
        
        Args:
            category: Filter articles by category
            limit: Number of articles to return
            offset: Offset for pagination
            
        Returns:
            List[Dict[str, Any]]: List of articles
        """
        try:
            # Create cache key
            cache_key = f"articles:{category or 'all'}:{limit}:{offset}"
            
            # Try to get from cache first
            cached_data = self.cache_service.get(cache_key)
            if cached_data:
                logger.info(f"Articles found in cache for key: {cache_key}")
                return json.loads(cached_data)
            
            # If not in cache, get from database
            logger.info(f"Fetching articles from database for category: {category}")
            
            # Simulate database query delay
            await asyncio.sleep(0.1)
            
            # In a real implementation, you would query the database:
            # db = SessionLocal()
            # query = db.query(Article).filter(Article.is_published == True)
            # if category:
            #     query = query.filter(Article.category == category)
            # articles = query.offset(offset).limit(limit).all()
            
            # For now, we'll simulate articles
            articles = []
            start_id = offset + 1
            for i in range(limit):
                article_id = start_id + i
                articles.append({
                    "id": article_id,
                    "title": f"Sample Article {article_id}",
                    "content": f"This is the content of sample article {article_id}. " * 10,
                    "category": category or "general",
                    "author": f"Author {article_id % 5 + 1}",
                    "published_at": "2023-01-01T12:00:00Z",
                    "views": article_id * 10
                })
            
            # Cache the results
            self.cache_service.set(cache_key, json.dumps(articles), settings.CACHE_TTL)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching articles: {e}")
            return []
    
    async def get_article(self, article_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific article by ID.
        
        Args:
            article_id: Article ID
            
        Returns:
            Dict[str, Any]: Article data or None if not found
        """
        try:
            # Create cache key
            cache_key = f"article:{article_id}"
            
            # Try to get from cache first
            cached_data = self.cache_service.get(cache_key)
            if cached_data:
                logger.info(f"Article {article_id} found in cache")
                return json.loads(cached_data)
            
            # If not in cache, get from database
            logger.info(f"Fetching article {article_id} from database")
            
            # Simulate database query delay
            await asyncio.sleep(0.05)
            
            # In a real implementation, you would query the database:
            # db = SessionLocal()
            # article = db.query(Article).filter(Article.id == article_id, Article.is_published == True).first()
            
            # For now, we'll simulate an article
            article = {
                "id": article_id,
                "title": f"Sample Article {article_id}",
                "content": f"This is the detailed content of sample article {article_id}. " * 50,
                "category": "technology",
                "author": f"Author {article_id % 5 + 1}",
                "published_at": "2023-01-01T12:00:00Z",
                "views": article_id * 10
            }
            
            # Cache the result
            self.cache_service.set(cache_key, json.dumps(article), settings.CACHE_TTL)
            
            return article
            
        except Exception as e:
            logger.error(f"Error fetching article {article_id}: {e}")
            return None
    
    async def record_view(self, article_id: int) -> bool:
        """
        Record a view for an article.
        
        Args:
            article_id: Article ID
            
        Returns:
            bool: True if successful
        """
        try:
            # In a real implementation, you would update the database:
            # db = SessionLocal()
            # article = db.query(Article).filter(Article.id == article_id).first()
            # if article:
            #     article.views += 1
            #     db.commit()
            #     return True
            # return False
            
            # For now, we'll just log the view
            logger.info(f"Recorded view for article {article_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error recording view for article {article_id}: {e}")
            return False