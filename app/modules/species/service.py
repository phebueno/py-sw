from typing import Optional, Dict, Any
from app.core.swapi_client import swapi_client


class SpeciesService:
    """Lógica de negócio para espécies"""

    @staticmethod
    async def get_species(species_id: int) -> Dict[str, Any]:
        """
        Busca uma espécie específica por ID
        """
        data = await swapi_client._make_request(f"species/{species_id}")
        return data

    @staticmethod
    async def search_species(
        search: Optional[str] = None,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Lista espécies com paginação e busca
        """
        params = {"page": page}

        if search:
            params["search"] = search

        data = await swapi_client._make_request("species", params)
        return data
