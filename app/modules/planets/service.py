from typing import Optional, Dict, Any
from app.core.swapi_client import swapi_client


class PlanetService:
    """Lógica de negócio para planetas"""

    @staticmethod
    async def get_planet(planet_id: int) -> Dict[str, Any]:
        """
        Busca um planeta específico
        """
        data = await swapi_client._make_request(f"planets/{planet_id}")
        return data

    @staticmethod
    async def search_planets(
        search: Optional[str] = None,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Lista planetas com filtros

        - search
        - page
        """
        params = {"page": page}

        if search:
            params["search"] = search

        data = await swapi_client._make_request("planets", params)
        return data
