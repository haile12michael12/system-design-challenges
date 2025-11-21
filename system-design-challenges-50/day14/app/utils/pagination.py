from typing import List, TypeVar, Generic

T = TypeVar('T')

class Pagination:
    def __init__(self, items: List[T], total: int, page: int, size: int):
        self.items = items
        self.total = total
        self.page = page
        self.size = size
        self.pages = (total + size - 1) // size

def paginate(items: List[T], page: int, size: int) -> Pagination:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * size
    end = start + size
    paginated_items = items[start:end]
    return Pagination(paginated_items, total, page, size)