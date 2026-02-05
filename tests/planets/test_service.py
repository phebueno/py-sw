import pytest
from unittest.mock import AsyncMock, patch
from app.modules.planets.service import PlanetService
from tests.planets.factories import make_planet


@pytest.mark.asyncio
async def test_get_planet():
    planet_data = make_planet({"name": "Alderaan"})
    
    with patch("app.modules.planets.service.swapi_client._make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = planet_data
        
        response = await PlanetService.get_planet(1)
        
        mock_request.assert_awaited_once_with("planets/1")
        assert response["name"] == "Alderaan"


@pytest.mark.asyncio
async def test_search_planets_without_search():
    planet_data = {"results": [make_planet()], "count": 1}
    
    with patch("app.modules.planets.service.swapi_client._make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = planet_data
        
        response = await PlanetService.search_planets(page=1)
        
        mock_request.assert_awaited_once_with("planets", {"page": 1})
        assert "results" in response
        assert len(response["results"]) == 1


@pytest.mark.asyncio
async def test_search_planets_with_search():
    planet_data = {"results": [make_planet({"name": "Hoth"})], "count": 1}
    
    with patch("app.modules.planets.service.swapi_client._make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = planet_data
        
        response = await PlanetService.search_planets(search="Hoth", page=2)
        
        mock_request.assert_awaited_once_with("planets", {"page": 2, "search": "Hoth"})
        assert response["results"][0]["name"] == "Hoth"
