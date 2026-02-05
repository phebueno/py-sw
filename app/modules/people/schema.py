from pydantic import BaseModel
from typing import List, Optional


class People(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str

    homeworld: str
    homeworld_id: Optional[str] = None
    person_id: Optional[str] = None

    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]

    created: str
    edited: str
    url: str
