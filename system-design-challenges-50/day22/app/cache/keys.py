"""Redis key definitions and helpers"""

def user_feed_key(user_id: int, cursor: str = None) -> str:
    """Generate key for user feed cache"""
    if cursor:
        return f"user_feed:{user_id}:{cursor}"
    return f"user_feed:{user_id}:initial"

def explore_feed_key(offset: int) -> str:
    """Generate key for explore feed cache"""
    return f"explore_feed:{offset}"

def user_profile_key(user_id: int) -> str:
    """Generate key for user profile cache"""
    return f"user_profile:{user_id}"

def post_key(post_id: int) -> str:
    """Generate key for post cache"""
    return f"post:{post_id}"

def trending_posts_key() -> str:
    """Generate key for trending posts cache"""
    return "trending_posts"

def rate_limit_key(user_id: int, action: str) -> str:
    """Generate key for rate limiting"""
    return f"rate_limit:{user_id}:{action}"