from typing import Optional, Dict, Any
from app.core.swapi_client import swapi_client


class StarshipService:
    """Lógica de negócio para naves"""

    @staticmethod
    async def get_starship(starship_id: int) -> Dict[str, Any]:
        """
        Busca uma nave específica por ID
        """
        data = await swapi_client._make_request(f"starships/{starship_id}")
        return data

    @staticmethod
    async def search_starships(
        search: Optional[str] = None,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Busca naves com filtros e paginação
        """
        params = {"page": page}
        if search:
            params["search"] = search

        data = await swapi_client._make_request("starships", params)
        return data
