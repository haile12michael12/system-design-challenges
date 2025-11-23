from app.config import settings
from typing import Dict, Any

class FeatureFlags:
    """Feature flag management utility"""
    
    # Default feature flag values
    DEFAULTS = {
        "cache_invalidation": True,
        "rollup_processing": True,
        "cost_optimization": True,
        "websocket_notifications": True,
        "email_digests": True,
        "advanced_analytics": False,
        "experimental_ui": False
    }
    
    def __init__(self):
        self.flags = self._load_flags()
    
    def _load_flags(self) -> Dict[str, bool]:
        """Load feature flags from configuration"""
        flags = self.DEFAULTS.copy()
        
        # Override with environment variables
        flags["cache_invalidation"] = settings.feature_cache_invalidation
        flags["rollup_processing"] = settings.feature_rollup_processing
        flags["cost_optimization"] = settings.feature_cost_optimization
        
        return flags
    
    def is_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.flags.get(feature, False)
    
    def enable(self, feature: str):
        """Enable a feature"""
        self.flags[feature] = True
    
    def disable(self, feature: str):
        """Disable a feature"""
        self.flags[feature] = False
    
    def get_all_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return self.flags.copy()

# Global feature flags instance
feature_flags = FeatureFlags()

def require_feature(feature: str):
    """Decorator to require a feature flag to be enabled"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not feature_flags.is_enabled(feature):
                raise Exception(f"Feature '{feature}' is not enabled")
            return func(*args, **kwargs)
        return wrapper
    return decorator