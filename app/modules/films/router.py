from typing import Optional
from fastapi import APIRouter, Path, Query
from app.modules.films.service import FilmService
from app.modules.films.schema import Film, FilmListResponse

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", summary="Listar filmes", response_model=FilmListResponse)
async def list_films(
    search: Optional[str] = Query(
        None,
        description="Buscar filme por título",
        examples="hope",
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
        examples=1,
    ),
):
    """
    Lista filmes da saga Star Wars com busca e paginação.

    A paginação é aplicada localmente, pois a SWAPI
    retorna todos os filmes de uma vez.
    """
    data = await FilmService.list_films(search=search, page=page)

    for film in data.get("results", []):
        film["film_id"] = film["url"].split("/")[-2]

    return data
@router.get("/{film_id}", summary="Buscar filme por ID", response_model=Film)
async def get_film(
    film_id: int = Path(
        ...,
        ge=1,
        description="ID do filme",
        examples=1,
    )
):
    """
    Busca um filme específico por ID.

    Exemplos:
    - 1: A New Hope
    - 2: The Empire Strikes Back
    - 3: Return of the Jedi
    """
    data = await FilmService.get_film(film_id)
    return data
