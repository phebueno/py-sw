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

class Vehicle(BaseModel):
    """Modelo de veículo do Star Wars"""
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
    vehicle_class: str
    pilots: List[str]
    films: List[str]
    created: str
    edited: str
    url: str
    
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