from typing import Any, Dict, Optional

from app.core.swapi_client import swapi_client


class VehicleService:
    """Lógica de negócio para veículos"""

    @staticmethod
    async def get_vehicle(vehicle_id: int) -> Dict[str, Any]:
        """
        Busca um veículo específico por ID
        """
        data = await swapi_client._make_request(f"vehicles/{vehicle_id}")
        return data

    @staticmethod
    async def search_vehicles(
        search: Optional[str] = None,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Busca veículos com filtros e paginação
        """
        params = {"page": page}
        if search:
            params["search"] = search

        data = await swapi_client._make_request("vehicles", params)
        return data
