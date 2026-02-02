from fastapi import APIRouter, Query, Path
from typing import Optional
from app.services.swapi_client import swapi_client

router = APIRouter(
    prefix="/people",
    tags=["People"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", summary="Listar personagens")
async def list_people(
    search: Optional[str] = Query(
        None, 
        description="Buscar personagem por nome",
        examples="luke"
    ),
    page: int = Query(
        1, 
        ge=1, 
        description="Número da página",
        examples=1
    )
):
    """
    Lista personagens do Star Wars com suporte a busca e paginação.
    
    - **search**: Nome do personagem (ex: luke, vader, leia)
    - **page**: Página de resultados (padrão: 1)
    
    Retorna dados paginados com informações detalhadas de cada personagem.
    """
    data = await swapi_client.get_people(search=search, page=page)
    
    for person in data.get("results", []):
        person["person_id"] = person["url"].split("/")[-2]
        person["homeworld_id"] = person["homeworld"].split("/")[-2]
    
    return data

@router.get("/{person_id}", summary="Buscar personagem por ID")
async def get_person(
    person_id: int = Path(
        ..., 
        ge=1, 
        description="ID do personagem",
        examples=1
    )
):
    """
    Busca um personagem específico por ID.
    
    - **person_id**: ID do personagem (1 = Luke Skywalker)
    
    Exemplos:
    - 1: Luke Skywalker
    - 4: Darth Vader
    - 5: Leia Organa
    """
    data = await swapi_client.get_person(person_id)
    
    return data