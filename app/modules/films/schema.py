from pydantic import BaseModel
from typing import List, Optional


class Film(BaseModel):
    """Modelo de filme do Star Wars"""

    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str
    characters: List[str]
    planets: List[str]
    starships: List[str]
    vehicles: List[str]
    species: List[str]
    created: str
    edited: str
    url: str

class FilmListResponse(BaseModel):
    """Resposta de lista de filmes"""

    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Film]
