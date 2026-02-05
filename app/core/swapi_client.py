from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException


class SWAPIClient:
    """Cliente HTTP para interagir com a API do Star Wars (SWAPI)"""

    BASE_URL = "https://swapi.dev/api"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0, headers={"User-Agent": "StarWars-API/1.0"})

    async def close(self):
        """Fecha o cliente HTTP"""
        await self.client.aclose()

    async def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição genérica à SWAPI

        Args:
            endpoint: Endpoint da API (ex: 'people', 'planets')
            params: Parâmetros de query

        Returns:
            Dados em formato JSON

        Raises:
            HTTPException: Se houver erro na requisição
        """
        try:
            url = f"{self.BASE_URL}/{endpoint}/"
            response = await self.client.get(url, params=params or {})
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Recurso não encontrado na SWAPI: {endpoint}",
                )
            raise HTTPException(
                status_code=e.response.status_code, detail=f"Erro na SWAPI: {str(e)}"
            )

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Timeout ao conectar com SWAPI")

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Erro ao conectar com SWAPI: {str(e)}")


swapi_client = SWAPIClient()
