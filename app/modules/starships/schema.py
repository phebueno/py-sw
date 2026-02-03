from pydantic import BaseModel
from typing import List

class Starship(BaseModel):
    """Modelo de nave do Star Wars"""
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: str
    MGLT: str
    starship_class: str
    pilots: List[str]
    films: List[str]
    created: str
    edited: str
    url: str