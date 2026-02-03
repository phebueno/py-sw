from typing import Optional
from fastapi import APIRouter, Path, Query
from app.modules.planets.service import PlanetService
from app.modules.planets.schema import Planet, PlanetListResponse

router = APIRouter(
    prefix="/planets",
    tags=["Planets"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Listar planetas", response_model=PlanetListResponse)
async def list_planets(
    search: Optional[str] = Query(
        None,
        description="Buscar planeta por nome",
        examples="tatooine",
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
        examples=1,
    ),
):
    """
    Lista planetas do universo Star Wars com busca e paginação.
    """
    data = await PlanetService.list_planets(search=search, page=page)

    for planet in data.get("results", []):
        planet["planet_id"] = planet["url"].split("/")[-2]

    return data


@router.get("/{planet_id}", summary="Buscar planeta por ID", response_model=Planet)
async def get_planet(
    planet_id: int = Path(
        ...,
        ge=1,
        description="ID do planeta",
        examples=1,
    )
):
    """
    Busca um planeta específico por ID.

    Exemplos:
    - 1: Tatooine
    - 2: Alderaan
    - 8: Naboo
    """
    return await PlanetService.get_planet(planet_id)
