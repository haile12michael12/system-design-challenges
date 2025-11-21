class CacheVersioning:
    @staticmethod
    def get_key_with_version(key: str, version: str = "v1") -> str:
        return f"{key}:{version}"
    
    @staticmethod
    def get_post_key(post_id: str, version: str = "v1") -> str:
        return f"post:{post_id}:{version}"
    
    @staticmethod
    def get_feed_key(user_id: str, version: str = "v1") -> str:
        return f"feed:{user_id}:{version}"