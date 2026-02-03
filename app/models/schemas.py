from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro"""

    detail: str
    status_code: int
