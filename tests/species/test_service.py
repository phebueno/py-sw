import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.modules.species.service import SpeciesService
from tests.species.factories import make_species
from tests.factories.pagination import make_paginated


@pytest.mark.asyncio
class TestSpeciesService:
    """Testes unitários para SpeciesService"""

    async def test_get_species_success(self):
        """Test getting a single species successfully"""
        species_id = 1
        species_data = make_species()

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=species_data)

            result = await SpeciesService.get_species(species_id)

            assert result is not None
            assert result["name"] == "Human"
            assert result["classification"] == "mammal"
            mock_client._make_request.assert_called_once_with("species/1")

    async def test_get_species_droid(self):
        """Test getting a different species (Droid)"""
        species_id = 2
        species_data = make_species(
            {
                "name": "Droid",
                "classification": "artificial",
                "designation": "sentient",
                "average_height": "varies",
                "url": "https://swapi.dev/api/species/2/",
            }
        )

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=species_data)

            result = await SpeciesService.get_species(species_id)

            assert result["name"] == "Droid"
            assert result["classification"] == "artificial"
            mock_client._make_request.assert_called_once_with("species/2")

    async def test_get_species_not_found(self):
        """Test getting a species that doesn't exist"""
        species_id = 999

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=404, detail="Not found")
            )

            with pytest.raises(HTTPException) as exc_info:
                await SpeciesService.get_species(species_id)

            assert exc_info.value.status_code == 404

    async def test_search_species_default(self):
        """Test searching species without parameters"""
        species_list = [make_species()]
        response = make_paginated(species_list)

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species()

            assert result is not None
            assert result["count"] > 0
            assert len(result["results"]) == 1
            assert result["results"][0]["name"] == "Human"
            mock_client._make_request.assert_called_once_with("species", {"page": 1})

    async def test_search_species_with_search_term(self):
        """Test searching species by name"""
        species_list = [make_species({"name": "Wookiee"})]
        response = make_paginated(species_list)

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species(search="Wookiee")

            assert result is not None
            assert result["results"][0]["name"] == "Wookiee"
            mock_client._make_request.assert_called_once_with(
                "species", {"page": 1, "search": "Wookiee"}
            )

    async def test_search_species_with_pagination(self):
        """Test pagination in species search"""
        species_list = [make_species()]
        response = make_paginated(
            species_list,
            next="https://swapi.dev/api/species/?page=3",
            previous="https://swapi.dev/api/species/?page=1",
        )

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species(page=2)

            assert result is not None
            assert result["next"] is not None
            assert result["previous"] is not None
            call_args = mock_client._make_request.call_args
            assert call_args[0][1]["page"] == 2

    async def test_search_species_with_search_and_pagination(self):
        """Test search with both search term and pagination"""
        species_list = [make_species({"name": "Yoda"})]
        response = make_paginated(species_list)

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species(search="Yoda", page=3)

            assert result is not None
            mock_client._make_request.assert_called_once_with(
                "species", {"page": 3, "search": "Yoda"}
            )

    async def test_search_species_empty_results(self):
        """Test search with no results"""

        response = make_paginated([])

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species(search="NonexistentSpecies")

            assert result["count"] == 0
            assert len(result["results"]) == 0

    async def test_search_species_connection_error(self):
        """Test search when connection fails"""
        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=503, detail="Service unavailable")
            )

            with pytest.raises(HTTPException) as exc_info:
                await SpeciesService.search_species()

            assert exc_info.value.status_code == 503

    async def test_search_species_multiple_results(self):
        """Test search returning multiple species"""
        species_list = [
            make_species({"name": "Human", "url": "https://swapi.dev/api/species/1/"}),
            make_species({"name": "Droid", "url": "https://swapi.dev/api/species/2/"}),
            make_species({"name": "Wookiee", "url": "https://swapi.dev/api/species/3/"}),
        ]
        response = make_paginated(species_list, count=3)

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await SpeciesService.search_species()

            assert result["count"] == 3
            assert len(result["results"]) == 3
            assert result["results"][0]["name"] == "Human"
            assert result["results"][1]["name"] == "Droid"
            assert result["results"][2]["name"] == "Wookiee"

    async def test_get_species_preserves_all_fields(self):
        """Test that all species fields are preserved"""
        species_data = make_species()

        with patch("app.modules.species.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=species_data)

            result = await SpeciesService.get_species(1)

            assert result["name"] == "Human"
            assert result["classification"] == "mammal"
            assert result["designation"] == "sentient"
            assert result["average_height"] == "180"
            assert result["skin_colors"] == "caucasian, black, asian, hispanic"
            assert result["hair_colors"] == "blonde, brown, black, red"
            assert result["eye_colors"] == "brown, blue, green, hazel"
            assert result["average_lifespan"] == "120"
            assert result["homeworld"] is not None
            assert result["language"] == "Galactic Basic"
            assert isinstance(result["people"], list)
            assert isinstance(result["films"], list)
            assert result["created"] == "2014-12-10T13:52:11.567000Z"
            assert result["edited"] == "2014-12-20T21:36:42.136000Z"
            assert result["url"] == "https://swapi.dev/api/species/1/"
