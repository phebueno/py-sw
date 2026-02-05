import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.modules.vehicles.service import VehicleService
from tests.vehicles.factories import make_vehicle
from tests.factories.pagination import make_paginated


@pytest.mark.asyncio
class TestVehicleService:
    """Testes unitários para VehicleService"""

    async def test_get_vehicle_success(self):
        """Test getting a single vehicle successfully"""

        vehicle_id = 4
        vehicle_data = make_vehicle()

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=vehicle_data)

            result = await VehicleService.get_vehicle(vehicle_id)

            assert result is not None
            assert result["name"] == "Sand Crawler"
            assert result["model"] == "Digger Crawler"
            assert result["vehicle_class"] == "wheeled"
            mock_client._make_request.assert_called_once_with("vehicles/4")

    async def test_get_vehicle_speeder(self):
        """Test getting a different vehicle (Speeder)"""

        vehicle_id = 6
        vehicle_data = make_vehicle(
            {
                "name": "T-16 skyhopper",
                "model": "T-16 skyhopper",
                "manufacturer": "Incom Corporation",
                "cost_in_credits": "14500",
                "vehicle_class": "repulsorcraft",
                "url": "https://swapi.dev/api/vehicles/6/",
            }
        )

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=vehicle_data)

            result = await VehicleService.get_vehicle(vehicle_id)

            assert result["name"] == "T-16 skyhopper"
            assert result["vehicle_class"] == "repulsorcraft"
            mock_client._make_request.assert_called_once_with("vehicles/6")

    async def test_get_vehicle_at_at(self):
        """Test getting AT-AT Walker"""

        vehicle_id = 18
        vehicle_data = make_vehicle(
            {
                "name": "AT-AT",
                "model": "All Terrain Armored Transport",
                "manufacturer": "Kuat Drive Yards, Imperial Department of Military Research",
                "cost_in_credits": "900000",
                "crew": "5",
                "passengers": "40",
                "cargo_capacity": "1000000",
                "vehicle_class": "walker",
                "length": "20",
                "url": "https://swapi.dev/api/vehicles/18/",
            }
        )

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=vehicle_data)

            result = await VehicleService.get_vehicle(vehicle_id)

            assert result["name"] == "AT-AT"
            assert result["vehicle_class"] == "walker"
            assert result["cargo_capacity"] == "1000000"

    async def test_get_vehicle_not_found(self):
        """Test getting a vehicle that doesn't exist"""

        vehicle_id = 999

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=404, detail="Not found")
            )

            with pytest.raises(HTTPException) as exc_info:
                await VehicleService.get_vehicle(vehicle_id)

            assert exc_info.value.status_code == 404

    async def test_search_vehicles_default(self):
        """Test searching vehicles without parameters"""

        vehicle_list = [make_vehicle()]
        response = make_paginated(vehicle_list)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles()

            assert result is not None
            assert result["count"] > 0
            assert len(result["results"]) == 1
            assert result["results"][0]["name"] == "Sand Crawler"
            mock_client._make_request.assert_called_once_with("vehicles", {"page": 1})

    async def test_search_vehicles_by_name(self):
        """Test searching vehicle by name"""

        vehicle_list = [make_vehicle({"name": "AT-ST"})]
        response = make_paginated(vehicle_list)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(search="AT-ST")

            assert result is not None
            assert result["results"][0]["name"] == "AT-ST"
            mock_client._make_request.assert_called_once_with(
                "vehicles", {"page": 1, "search": "AT-ST"}
            )

    async def test_search_vehicles_pagination(self):
        """Test pagination in vehicle search"""

        vehicle_list = [make_vehicle()]
        response = make_paginated(
            vehicle_list,
            next="https://swapi.dev/api/vehicles/?page=3",
            previous="https://swapi.dev/api/vehicles/?page=1",
        )

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(page=2)

            assert result is not None
            assert result["next"] is not None
            assert result["previous"] is not None
            call_args = mock_client._make_request.call_args
            assert call_args[0][1]["page"] == 2

    async def test_search_vehicles_with_search_and_pagination(self):
        """Test search with both search term and pagination"""

        vehicle_list = [make_vehicle({"name": "Speeder Bike"})]
        response = make_paginated(vehicle_list)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(search="Speeder Bike", page=3)

            assert result is not None
            mock_client._make_request.assert_called_once_with(
                "vehicles", {"page": 3, "search": "Speeder Bike"}
            )

    async def test_search_vehicles_empty_results(self):
        """Test search with no results"""

        response = make_paginated([])

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(search="NonexistentVehicle")

            assert result["count"] == 0
            assert len(result["results"]) == 0

    async def test_search_vehicles_connection_error(self):
        """Test search when connection fails"""

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=503, detail="Service unavailable")
            )

            with pytest.raises(HTTPException) as exc_info:
                await VehicleService.search_vehicles()

            assert exc_info.value.status_code == 503

    async def test_search_vehicles_multiple_results(self):
        """Test search returning multiple vehicles"""

        vehicle_list = [
            make_vehicle({"name": "Sand Crawler", "url": "https://swapi.dev/api/vehicles/4/"}),
            make_vehicle({"name": "AT-AT", "url": "https://swapi.dev/api/vehicles/18/"}),
            make_vehicle({"name": "AT-ST", "url": "https://swapi.dev/api/vehicles/19/"}),
        ]
        response = make_paginated(vehicle_list, count=3)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles()

            assert result["count"] == 3
            assert len(result["results"]) == 3
            assert result["results"][0]["name"] == "Sand Crawler"
            assert result["results"][1]["name"] == "AT-AT"
            assert result["results"][2]["name"] == "AT-ST"

    async def test_get_vehicle_preserves_all_fields(self):
        """Test that all vehicle fields are preserved"""

        vehicle_data = make_vehicle()

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=vehicle_data)

            result = await VehicleService.get_vehicle(4)

            assert result["name"] == "Sand Crawler"
            assert result["model"] == "Digger Crawler"
            assert result["manufacturer"] == "Corellia Mining Corporation"
            assert result["cost_in_credits"] == "150000"
            assert result["length"] == "36.8"
            assert result["max_atmosphering_speed"] == "30"
            assert result["crew"] == "46"
            assert result["passengers"] == "30"
            assert result["cargo_capacity"] == "50000"
            assert result["consumables"] == "2 months"
            assert result["vehicle_class"] == "wheeled"
            assert isinstance(result["pilots"], list)
            assert isinstance(result["films"], list)
            assert result["created"] == "2014-12-10T15:36:25.724000Z"
            assert result["edited"] == "2014-12-20T21:30:21.663000Z"
            assert result["url"] == "https://swapi.dev/api/vehicles/4/"

    async def test_search_vehicles_by_class(self):
        """Test searching vehicles by class (simulated)"""
        walker_list = [
            make_vehicle(
                {
                    "name": "AT-AT",
                    "vehicle_class": "walker",
                    "url": "https://swapi.dev/api/vehicles/18/",
                }
            ),
            make_vehicle(
                {
                    "name": "AT-ST",
                    "vehicle_class": "walker",
                    "url": "https://swapi.dev/api/vehicles/19/",
                }
            ),
        ]
        response = make_paginated(walker_list, count=2)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(search="walker")

            assert result["count"] == 2
            assert all(vehicle["vehicle_class"] == "walker" for vehicle in result["results"])

    async def test_search_vehicles_repulsorcraft(self):
        """Test searching repulsorcraft vehicles"""

        repulsor_list = [
            make_vehicle(
                {
                    "name": "T-16 skyhopper",
                    "vehicle_class": "repulsorcraft",
                    "url": "https://swapi.dev/api/vehicles/6/",
                }
            ),
            make_vehicle(
                {
                    "name": "X-34 landspeeder",
                    "vehicle_class": "repulsorcraft",
                    "url": "https://swapi.dev/api/vehicles/7/",
                }
            ),
        ]
        response = make_paginated(repulsor_list, count=2)

        with patch("app.modules.vehicles.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await VehicleService.search_vehicles(search="repulsorcraft")

            assert result["count"] == 2
            assert all(v["vehicle_class"] == "repulsorcraft" for v in result["results"])
