from typing import Optional
from fastapi import APIRouter, Path, Query
from app.models.schemas import PaginatedResponse
from app.modules.species.service import SpeciesService
from app.modules.species.schema import Species

router = APIRouter(
    prefix="/species",
    tags=["Species"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    summary="Listar espécies",
    response_model=PaginatedResponse[Species],
)
async def list_species(
    search: Optional[str] = Query(
        None,
        description="Buscar espécie pelo nome",
        examples=["wookiee"],
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
        examples=[1],
    ),
):
    """
    Lista espécies do universo Star Wars com paginação e busca.
    """
    return await SpeciesService.list_species(search=search, page=page)


@router.get(
    "/{species_id}",
    summary="Buscar espécie por ID",
    response_model=Species,
)
async def get_species(
    species_id: int = Path(
        ...,
        ge=1,
        description="ID da espécie",
        examples=[1],
    ),
):
    """
    Busca uma espécie específica pelo ID.
    """
    return await SpeciesService.get_species(species_id)
