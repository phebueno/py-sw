from pydantic import BaseModel
from typing import List, Optional


class PaginatedResponse(BaseModel):
    """Resposta paginada padrão da SWAPI"""

    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[dict]


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro"""

    detail: str
    status_code: int
