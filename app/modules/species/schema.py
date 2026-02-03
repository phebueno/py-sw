from pydantic import BaseModel
from typing import List


class Species(BaseModel):
    """Modelo de espécie do Star Wars"""

    name: str
    classification: str
    designation: str
    average_height: str
    skin_colors: str
    hair_colors: str
    eye_colors: str
    average_lifespan: str
    homeworld: str | None
    language: str
    people: List[str]
    films: List[str]
    created: str
    edited: str
    url: str
