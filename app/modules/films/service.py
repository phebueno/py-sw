from typing import Dict, Any, Optional
from app.core.swapi_client import swapi_client


class FilmService:
    """Lógica de negócio para filmes"""

    @staticmethod
    async def list_films(
        search: Optional[str] = None,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Lista filmes com filtros

        Mesmo padrão de people:
        - page
        - search
        """
        params = {"page": page}

        if search:
            params["search"] = search

        data = await swapi_client._make_request("films", params)
        return data

    @staticmethod
    async def get_film(film_id: int) -> Dict[str, Any]:
        """
        Busca um filme específico por ID
        """
        data = await swapi_client._make_request(f"films/{film_id}")
        return data
