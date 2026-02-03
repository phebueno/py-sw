from typing import Optional
from fastapi import APIRouter, Path, Query
from app.models.schemas import PaginatedResponse
from app.modules.starships.service import StarshipService
from app.modules.starships.schema import Starship

router = APIRouter(
    prefix="/starships",
    tags=["Starships"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    summary="Listar naves",
    response_model=PaginatedResponse[Starship],
)
async def list_starships(
    search: Optional[str] = Query(
        None,
        description="Buscar nave por nome ou modelo",
        examples=["falcon"],
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
        examples=1,
    ),
):
    """
    Lista naves do universo Star Wars com suporte a busca e paginação.
    """
    data = await StarshipService.search_starships(search=search, page=page)

    for starship in data.get("results", []):
        starship["starship_id"] = starship["url"].split("/")[-2]

    return data


@router.get(
    "/{starship_id}",
    summary="Buscar nave por ID",
    response_model=Starship,
)
async def get_starship(
    starship_id: int = Path(
        ...,
        ge=1,
        description="ID da nave",
        examples=9,
    )
):
    """
    Busca uma nave específica por ID.

    Exemplo:
    - 9: Death Star
    - 10: Millennium Falcon
    """
    data = await StarshipService.get_starship(starship_id)
    return data
