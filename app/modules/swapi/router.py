from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional

from app.modules.people.service import PeopleService
from app.modules.planets.service import PlanetService
from app.modules.films.service import FilmService
from app.modules.starships.service import StarshipService
from app.modules.vehicles.service import VehicleService
from app.modules.species.service import SpeciesService

router = APIRouter(
    prefix="/swapi",
    tags=["SWAPI"],
)

RESOURCE_MAP = {
    "people": PeopleService.search_people,
    "planets": PlanetService.search_planets,
    "films": FilmService.search_films,
    "starships": StarshipService.search_starships,
    "vehicles": VehicleService.search_vehicles,
    "species": SpeciesService.search_species,
}

@router.get("/{resource}")
async def generic_search(
    resource: str = Path(..., description="Recurso da SWAPI"),
    search: Optional[str] = Query(None, description="Texto de busca"),
    page: int = Query(1, ge=1)
):
    """
    Endpoint genérico para consulta de recursos da SWAPI.
    
    Exemplos:
    - /swapi/people?search=luke
    - /swapi/planets?search=tatooine
    - /swapi/starships?search=death
    """

    service = RESOURCE_MAP.get(resource)

    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Recurso '{resource}' não é suportado"
        )

    return await service(search=search, page=page)
