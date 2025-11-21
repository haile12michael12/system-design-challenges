class TTLPolicy:
    POST_TTL = 3600  # 1 hour
    FEED_TTL = 1800   # 30 minutes
    USER_TTL = 7200   # 2 hours
    
    @classmethod
    def get_post_ttl(cls) -> int:
        return cls.POST_TTL
    
    @classmethod
    def get_feed_ttl(cls) -> int:
        return cls.FEED_TTL
    
    @classmethod
    def get_user_ttl(cls) -> int:
        return cls.USER_TTL