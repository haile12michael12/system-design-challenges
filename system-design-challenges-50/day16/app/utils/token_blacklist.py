import redis
from datetime import datetime, timedelta
from ..core.config import settings

class TokenBlacklist:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)

    def blacklist_token(self, token: str, expires_at: datetime) -> None:
        """Add a token to the blacklist."""
        # Calculate remaining time until expiration
        now = datetime.utcnow()
        expiry_seconds = int((expires_at - now).total_seconds())
        
        if expiry_seconds > 0:
            self.redis_client.setex(f"blacklisted:{token}", expiry_seconds, "true")

    def is_token_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted."""
        return self.redis_client.exists(f"blacklisted:{token}") > 0

    def remove_expired_tokens(self) -> None:
        """Remove expired tokens from the blacklist."""
        # Redis automatically expires keys, so this is handled automatically
        pass