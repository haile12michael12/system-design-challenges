from dataclasses import dataclass

@dataclass
class FeedQuery:
    skip: int = 0
    limit: int = 10