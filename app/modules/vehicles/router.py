from typing import Optional

from fastapi import APIRouter, Path, Query

from app.models.schemas import PaginatedResponse
from app.modules.vehicles.schema import Vehicle
from app.modules.vehicles.service import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    summary="Listar veículos",
    response_model=PaginatedResponse[Vehicle],
)
async def list_vehicles(
    search: Optional[str] = Query(
        None,
        description="Buscar veículo por nome ou modelo",
        examples=["speeder"],
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página",
        examples=1,
    ),
):
    """
    Lista veículos do universo Star Wars com suporte a busca e paginação.
    """
    data = await VehicleService.search_vehicles(search=search, page=page)

    for vehicle in data.get("results", []):
        vehicle["vehicle_id"] = vehicle["url"].split("/")[-2]

    return data


@router.get(
    "/{vehicle_id}",
    summary="Buscar veículo por ID",
    response_model=Vehicle,
)
async def get_vehicle(
    vehicle_id: int = Path(
        ...,
        ge=1,
        description="ID do veículo",
        examples=4,
    )
):
    """
    Busca um veículo específico por ID.

    Exemplos:
    - 4: Sand Crawler
    - 6: T-16 skyhopper
    """
    data = await VehicleService.get_vehicle(vehicle_id)
    return data
