from typing import Optional, Dict, Any
from app.core.swapi_client import swapi_client


class PeopleService:
    """Lógica de negócio para personagens"""

    @staticmethod
    async def get_person(person_id: int) -> Dict[str, Any]:
        """
        Busca um personagem específico

        Responsabilidades:
        - Validar entrada
        - Chamar o client
        - Transformar dados (aplicar regras de negócio)
        - Retornar no schema correto
        """

        data = await swapi_client._make_request(f"people/{person_id}")
        return data

    @staticmethod
    async def search_people(
        search: Optional[str] = None, page: int = 1
    ) -> Dict[str, Any]:
        """
        Busca personagens com filtros

        Pode aplicar:
        - Filtros customizados
        - Enriquecimento de dados
        - Lógica de negócio complexa
        - Cache
        """
        params = {"page": page}
        if search:
            params["search"] = search

        data = await swapi_client._make_request("people", params)

        return data
