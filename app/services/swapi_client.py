import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException

class SWAPIClient:
    """Cliente para interagir com a API do Star Wars (SWAPI)"""
    
    BASE_URL = "https://swapi.dev/api"
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=10.0,
            headers={"User-Agent": "StarWars-API/1.0"}
        )
    
    async def close(self):
        """Fecha o cliente HTTP"""
        await self.client.aclose()
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição à SWAPI
        
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
                    detail=f"Recurso não encontrado na SWAPI: {endpoint}"
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erro na SWAPI: {str(e)}"
            )
        
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Timeout ao conectar com SWAPI"
            )
        
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Erro ao conectar com SWAPI: {str(e)}"
            )
    
    async def get_people(
        self, 
        search: Optional[str] = None, 
        page: int = 1
    ) -> Dict[str, Any]:
        """Busca personagens"""
        params = {"page": page}
        if search:
            params["search"] = search
        return await self._make_request("people", params)
    
    async def get_person(self, person_id: int) -> Dict[str, Any]:
        """Busca personagem por ID"""
        return await self._make_request(f"people/{person_id}")
    
swapi_client = SWAPIClient()