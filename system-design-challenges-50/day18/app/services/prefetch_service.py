from typing import List, Optional, Dict, Any
import asyncio
import json

from ..services.news_service import NewsService
from ..services.cache import get_cache_service
from ..db.models import UserPreference
from ..db.session import SessionLocal
from ..core.config import settings
from ..core.logging import logger


class PrefetchService:
    """Service for prefetching news articles based on user preferences."""
    
    def __init__(self):
        self.cache_service = get_cache_service()
        self.news_service = NewsService()
    
    async def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user preferences for prefetching.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict[str, Any]: User preferences or None if not found
        """
        try:
            # Create cache key
            cache_key = f"user_prefs:{user_id}"
            
            # Try to get from cache first
            cached_data = self.cache_service.get(cache_key)
            if cached_data:
                logger.info(f"User preferences found in cache for user: {user_id}")
                return json.loads(cached_data)
            
            # If not in cache, get from database
            logger.info(f"Fetching user preferences from database for user: {user_id}")
            
            # In a real implementation, you would query the database:
            # db = SessionLocal()
            # prefs = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
            
            # For now, we'll simulate user preferences
            preferences = {
                "preferred_categories": ["technology", "science", "business"],
                "preferred_authors": ["Author 1", "Author 3"]
            }
            
            # Cache the results
            self.cache_service.set(cache_key, json.dumps(preferences), settings.CACHE_TTL)
            
            return preferences
            
        except Exception as e:
            logger.error(f"Error fetching user preferences for user {user_id}: {e}")
            return None
    
    async def get_prefetched_articles(self, category: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get prefetched articles based on user preferences.
        
        Args:
            category: Filter articles by category
            limit: Number of articles to return
            offset: Offset for pagination
            
        Returns:
            List[Dict[str, Any]]: List of prefetched articles
        """
        try:
            # For demonstration, we'll use a default user ID
            # In a real implementation, this would come from authentication
            user_id = "default_user"
            
            # Get user preferences
            preferences = await self.get_user_preferences(user_id)
            
            # Create cache key
            cache_key = f"prefetched_articles:{user_id}:{category or 'all'}:{limit}:{offset}"
            
            # Try to get from cache first
            cached_data = self.cache_service.get(cache_key)
            if cached_data:
                logger.info(f"Prefetched articles found in cache for user: {user_id}")
                return json.loads(cached_data)
            
            # If not in cache, generate prefetched articles
            logger.info(f"Generating prefetched articles for user: {user_id}")
            
            # Get articles based on preferences
            articles = []
            
            if preferences:
                # Get articles from preferred categories
                preferred_categories = preferences.get("preferred_categories", [])
                
                # Distribute limit among preferred categories
                category_limit = max(1, limit // len(preferred_categories)) if preferred_categories else limit
                
                for pref_category in preferred_categories:
                    if len(articles) >= limit:
                        break
                        
                    # Get articles for this category
                    category_articles = await self.news_service.get_articles(
                        category=pref_category, 
                        limit=category_limit, 
                        offset=offset
                    )
                    
                    # Add to results
                    for article in category_articles:
                        if len(articles) >= limit:
                            break
                        articles.append(article)
            
            # If we don't have enough articles, fill with general articles
            if len(articles) < limit:
                remaining = limit - len(articles)
                general_articles = await self.news_service.get_articles(
                    category=category,
                    limit=remaining,
                    offset=offset
                )
                articles.extend(general_articles[:remaining])
            
            # Cache the results
            self.cache_service.set(cache_key, json.dumps(articles), settings.CACHE_TTL)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error generating prefetched articles: {e}")
            # Fallback to regular news service
            return await self.news_service.get_articles(category, limit, offset)
    
    async def prefetch_for_user(self, user_id: str) -> bool:
        """
        Prefetch articles for a user in the background.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Starting prefetch for user: {user_id}")
            
            # Generate prefetched articles (this will cache them)
            articles = await self.get_prefetched_articles(limit=settings.PREFETCH_LIMIT)
            
            logger.info(f"Prefetched {len(articles)} articles for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error prefetching articles for user {user_id}: {e}")
            return False