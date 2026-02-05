from typing import List, TypeVar, Callable

T = TypeVar("T")

def make_paginated(
    items: List[T],
    count: int | None = None,
    next: str | None = None,
    previous: str | None = None,
):
    return {
        "count": count or len(items),
        "next": next,
        "previous": previous,
        "results": items,
    }
