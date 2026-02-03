from pydantic import BaseModel
from typing import List, Optional


class Planet(BaseModel):
    """Modelo de planeta do Star Wars"""

    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    climate: str
    gravity: str
    terrain: str
    surface_water: str
    population: str
    residents: List[str]
    films: List[str]
    created: str
    edited: str
    url: str

class PlanetListResponse(BaseModel):
    """Resposta paginada de planetas"""

    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Planet]