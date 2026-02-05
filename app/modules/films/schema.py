from typing import List, Optional

from pydantic import BaseModel


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
