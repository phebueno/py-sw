import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.modules.starships.service import StarshipService
from tests.starships.factories import make_starship
from tests.factories.pagination import make_paginated


@pytest.mark.asyncio
class TestStarshipService:
    """Testes unitários para StarshipService"""

    async def test_get_starship_success(self):
        """Test getting a single starship successfully"""

        starship_id = 12
        starship_data = make_starship()

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=starship_data)

            result = await StarshipService.get_starship(starship_id)

            assert result is not None
            assert result["name"] == "X-wing"
            assert result["model"] == "T-65 X-wing starfighter"
            assert result["starship_class"] == "Starfighter"
            mock_client._make_request.assert_called_once_with("starships/12")

    async def test_get_starship_millennium_falcon(self):
        """Test getting a different starship (Millennium Falcon)"""

        starship_id = 10
        starship_data = make_starship(
            {
                "name": "Millennium Falcon",
                "model": "YT-1300 light freighter",
                "manufacturer": "Corellian Engineering Corporation",
                "cost_in_credits": "100000",
                "starship_class": "Light freighter",
                "url": "https://swapi.dev/api/starships/10/",
            }
        )

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=starship_data)

            result = await StarshipService.get_starship(starship_id)

            assert result["name"] == "Millennium Falcon"
            assert result["model"] == "YT-1300 light freighter"
            assert result["starship_class"] == "Light freighter"
            mock_client._make_request.assert_called_once_with("starships/10")

    async def test_get_starship_star_destroyer(self):
        """Test getting Star Destroyer"""

        starship_id = 3
        starship_data = make_starship(
            {
                "name": "Star Destroyer",
                "model": "Imperial I-class Star Destroyer",
                "manufacturer": "Kuat Drive Yards",
                "cost_in_credits": "1000000000",
                "crew": "37465",
                "passengers": "36000",
                "starship_class": "Star Destroyer",
                "length": "1600",
                "url": "https://swapi.dev/api/starships/3/",
            }
        )

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=starship_data)

            result = await StarshipService.get_starship(starship_id)

            assert result["name"] == "Star Destroyer"
            assert result["cost_in_credits"] == "1000000000"
            assert int(result["crew"]) > 1000

    async def test_get_starship_not_found(self):
        """Test getting a starship that doesn't exist"""

        starship_id = 999

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=404, detail="Not found")
            )

            with pytest.raises(HTTPException) as exc_info:
                await StarshipService.get_starship(starship_id)

            assert exc_info.value.status_code == 404

    async def test_search_starships_default(self):
        """Test searching starships without parameters"""

        starship_list = [make_starship()]
        response = make_paginated(starship_list)

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships()

            assert result is not None
            assert result["count"] > 0
            assert len(result["results"]) == 1
            assert result["results"][0]["name"] == "X-wing"
            mock_client._make_request.assert_called_once_with("starships", {"page": 1})

    async def test_search_starships_by_name(self):
        """Test searching starship by name"""

        starship_list = [make_starship({"name": "Millennium Falcon"})]
        response = make_paginated(starship_list)

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships(search="Millennium Falcon")

            assert result is not None
            assert result["results"][0]["name"] == "Millennium Falcon"
            mock_client._make_request.assert_called_once_with(
                "starships", {"page": 1, "search": "Millennium Falcon"}
            )

    async def test_search_starships_pagination(self):
        """Test pagination in starship search"""

        starship_list = [make_starship()]
        response = make_paginated(
            starship_list,
            next="https://swapi.dev/api/starships/?page=3",
            previous="https://swapi.dev/api/starships/?page=1",
        )

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships(page=2)

            assert result is not None
            assert result["next"] is not None
            assert result["previous"] is not None
            call_args = mock_client._make_request.call_args
            assert call_args[0][1]["page"] == 2

    async def test_search_starships_with_search_and_pagination(self):
        """Test search with both search term and pagination"""
        starship_list = [make_starship({"name": "TIE Fighter"})]
        response = make_paginated(starship_list)

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships(search="TIE Fighter", page=3)

            assert result is not None
            mock_client._make_request.assert_called_once_with(
                "starships", {"page": 3, "search": "TIE Fighter"}
            )

    async def test_search_starships_empty_results(self):
        """Test search with no results"""
        response = make_paginated([])

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships(search="NonexistentStarship")

            assert result["count"] == 0
            assert len(result["results"]) == 0

    async def test_search_starships_connection_error(self):
        """Test search when connection fails"""
        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=503, detail="Service unavailable")
            )

            with pytest.raises(HTTPException) as exc_info:
                await StarshipService.search_starships()

            assert exc_info.value.status_code == 503

    async def test_search_starships_multiple_results(self):
        """Test search returning multiple starships"""
        starship_list = [
            make_starship({"name": "X-wing", "url": "https://swapi.dev/api/starships/12/"}),
            make_starship(
                {"name": "Millennium Falcon", "url": "https://swapi.dev/api/starships/10/"}
            ),
            make_starship({"name": "TIE Fighter", "url": "https://swapi.dev/api/starships/13/"}),
        ]
        response = make_paginated(starship_list, count=3)

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships()

            assert result["count"] == 3
            assert len(result["results"]) == 3
            assert result["results"][0]["name"] == "X-wing"
            assert result["results"][1]["name"] == "Millennium Falcon"
            assert result["results"][2]["name"] == "TIE Fighter"

    async def test_get_starship_preserves_all_fields(self):
        """Test that all starship fields are preserved"""

        starship_data = make_starship()

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=starship_data)

            result = await StarshipService.get_starship(12)

            assert result["name"] == "X-wing"
            assert result["model"] == "T-65 X-wing starfighter"
            assert result["manufacturer"] == "Incom Corporation"
            assert result["cost_in_credits"] == "149999"
            assert result["length"] == "12.9"
            assert result["max_atmosphering_speed"] == "1050"
            assert result["crew"] == "1"
            assert result["passengers"] == "0"
            assert result["cargo_capacity"] == "64"
            assert result["consumables"] == "5 days"
            assert result["hyperdrive_rating"] == "1.0"
            assert result["MGLT"] == "100"
            assert result["starship_class"] == "Starfighter"
            assert isinstance(result["pilots"], list)
            assert isinstance(result["films"], list)
            assert result["created"] == "2014-12-12T11:19:05.340000Z"
            assert result["edited"] == "2014-12-20T21:23:49.886000Z"
            assert result["url"] == "https://swapi.dev/api/starships/12/"

    async def test_search_starships_by_class(self):
        """Test searching starships by class (simulated)"""
        starfighter_list = [
            make_starship(
                {
                    "name": "X-wing",
                    "starship_class": "Starfighter",
                    "url": "https://swapi.dev/api/starships/12/",
                }
            ),
            make_starship(
                {
                    "name": "TIE Fighter",
                    "starship_class": "Starfighter",
                    "url": "https://swapi.dev/api/starships/13/",
                }
            ),
        ]
        response = make_paginated(starfighter_list, count=2)

        with patch("app.modules.starships.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await StarshipService.search_starships(search="starfighter")

            assert result["count"] == 2
            assert all(ship["starship_class"] == "Starfighter" for ship in result["results"])
