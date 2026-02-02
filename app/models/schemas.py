from pydantic import BaseModel, Field
from typing import List, Optional

class People(BaseModel):
    """Modelo de personagem do Star Wars"""
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]
    created: str
    edited: str
    url: str

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