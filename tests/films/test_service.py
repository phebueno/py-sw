import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.modules.films.service import FilmService
from tests.films.factories import make_film
from tests.factories.pagination import make_paginated


@pytest.mark.asyncio
class TestFilmService:
    """Testes unitários para FilmService"""

    async def test_get_film_success(self):
        """Test getting a single film successfully"""

        film_id = 1
        film_data = make_film()

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=film_data)

            result = await FilmService.get_film(film_id)

            assert result is not None
            assert result["title"] == "A New Hope"
            assert result["episode_id"] == 4
            assert result["director"] == "George Lucas"
            mock_client._make_request.assert_called_once_with("films/1")

    async def test_get_film_empire_strikes_back(self):
        """Test getting The Empire Strikes Back"""

        film_id = 2
        film_data = make_film(
            {
                "title": "The Empire Strikes Back",
                "episode_id": 5,
                "director": "Irvin Kershner",
                "release_date": "1980-05-17",
                "url": "https://swapi.dev/api/films/2/",
            }
        )

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=film_data)

            result = await FilmService.get_film(film_id)

            assert result["title"] == "The Empire Strikes Back"
            assert result["episode_id"] == 5
            assert result["director"] == "Irvin Kershner"

    async def test_get_film_return_of_jedi(self):
        """Test getting Return of the Jedi"""

        film_id = 3
        film_data = make_film(
            {
                "title": "Return of the Jedi",
                "episode_id": 6,
                "director": "Richard Marquardt",
                "release_date": "1983-05-25",
                "url": "https://swapi.dev/api/films/3/",
            }
        )

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=film_data)

            result = await FilmService.get_film(film_id)

            assert result["title"] == "Return of the Jedi"
            assert result["episode_id"] == 6

    async def test_get_film_phantom_menace(self):
        """Test getting The Phantom Menace"""

        film_id = 4
        film_data = make_film(
            {
                "title": "The Phantom Menace",
                "episode_id": 1,
                "director": "George Lucas",
                "release_date": "1999-05-19",
                "url": "https://swapi.dev/api/films/4/",
            }
        )

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=film_data)

            result = await FilmService.get_film(film_id)

            assert result["title"] == "The Phantom Menace"
            assert result["episode_id"] == 1

    async def test_get_film_not_found(self):
        """Test getting a film that doesn't exist"""

        film_id = 999

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=404, detail="Not found")
            )

            with pytest.raises(HTTPException) as exc_info:
                await FilmService.get_film(film_id)

            assert exc_info.value.status_code == 404

    async def test_search_films_default(self):
        """Test searching films without parameters"""

        film_list = [make_film()]
        response = make_paginated(film_list)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films()

            assert result is not None
            assert result["count"] > 0
            assert len(result["results"]) == 1
            assert result["results"][0]["title"] == "A New Hope"
            mock_client._make_request.assert_called_once_with("films", {"page": 1})

    async def test_search_films_by_title(self):
        """Test searching film by title"""

        film_list = [make_film({"title": "The Force Awakens"})]
        response = make_paginated(film_list)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(search="The Force Awakens")

            assert result is not None
            assert result["results"][0]["title"] == "The Force Awakens"
            mock_client._make_request.assert_called_once_with(
                "films", {"page": 1, "search": "The Force Awakens"}
            )

    async def test_search_films_pagination(self):
        """Test pagination in film search"""

        film_list = [make_film()]
        response = make_paginated(
            film_list,
            next="https://swapi.dev/api/films/?page=2",
            previous=None,
        )

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(page=1)

            assert result is not None
            assert result["next"] is not None
            call_args = mock_client._make_request.call_args
            assert call_args[0][1]["page"] == 1

    async def test_search_films_with_search_and_pagination(self):
        """Test search with both search term and pagination"""

        film_list = [make_film({"title": "Empire"})]
        response = make_paginated(film_list)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(search="Empire", page=2)

            assert result is not None
            mock_client._make_request.assert_called_once_with(
                "films", {"page": 2, "search": "Empire"}
            )

    async def test_search_films_empty_results(self):
        """Test search with no results"""

        response = make_paginated([])

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(search="NonexistentFilm")

            assert result["count"] == 0
            assert len(result["results"]) == 0

    async def test_search_films_connection_error(self):
        """Test search when connection fails"""

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(
                side_effect=HTTPException(status_code=503, detail="Service unavailable")
            )

            with pytest.raises(HTTPException) as exc_info:
                await FilmService.search_films()

            assert exc_info.value.status_code == 503

    async def test_search_films_all_original_trilogy(self):
        """Test search returning all original trilogy films"""

        film_list = [
            make_film(
                {
                    "title": "A New Hope",
                    "episode_id": 4,
                    "url": "https://swapi.dev/api/films/1/",
                }
            ),
            make_film(
                {
                    "title": "The Empire Strikes Back",
                    "episode_id": 5,
                    "url": "https://swapi.dev/api/films/2/",
                }
            ),
            make_film(
                {
                    "title": "Return of the Jedi",
                    "episode_id": 6,
                    "url": "https://swapi.dev/api/films/3/",
                }
            ),
        ]
        response = make_paginated(film_list, count=3)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films()

            assert result["count"] == 3
            assert len(result["results"]) == 3
            assert result["results"][0]["episode_id"] == 4
            assert result["results"][1]["episode_id"] == 5
            assert result["results"][2]["episode_id"] == 6

    async def test_get_film_preserves_all_fields(self):
        """Test that all film fields are preserved"""

        film_data = make_film()

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=film_data)

            result = await FilmService.get_film(1)

            assert result["title"] == "A New Hope"
            assert result["episode_id"] == 4
            assert result["director"] == "George Lucas"
            assert result["producer"] == "Gary Kurtz, Rick McCallum"
            assert result["release_date"] == "1977-05-25"
            assert "opening_crawl" in result
            assert len(result["opening_crawl"]) > 0
            assert isinstance(result["characters"], list)
            assert isinstance(result["planets"], list)
            assert isinstance(result["starships"], list)
            assert isinstance(result["vehicles"], list)
            assert isinstance(result["species"], list)
            assert result["created"] == "2014-12-10T14:23:13.671000Z"
            assert result["edited"] == "2014-12-20T19:49:45.256000Z"
            assert result["url"] == "https://swapi.dev/api/films/1/"

    async def test_search_films_by_director(self):
        """Test searching films by director (simulated)"""
        lucas_films = [
            make_film(
                {
                    "title": "A New Hope",
                    "director": "George Lucas",
                    "url": "https://swapi.dev/api/films/1/",
                }
            ),
            make_film(
                {
                    "title": "The Phantom Menace",
                    "director": "George Lucas",
                    "url": "https://swapi.dev/api/films/4/",
                }
            ),
        ]
        response = make_paginated(lucas_films, count=2)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(search="George Lucas")

            assert result["count"] == 2
            assert all(film["director"] == "George Lucas" for film in result["results"])

    async def test_search_films_by_year(self):
        """Test searching films by release year (simulated)"""
        prequels = [
            make_film(
                {
                    "title": "The Phantom Menace",
                    "episode_id": 1,
                    "release_date": "1999-05-19",
                    "url": "https://swapi.dev/api/films/4/",
                }
            ),
            make_film(
                {
                    "title": "Attack of the Clones",
                    "episode_id": 2,
                    "release_date": "2002-05-16",
                    "url": "https://swapi.dev/api/films/5/",
                }
            ),
        ]
        response = make_paginated(prequels, count=2)

        with patch("app.modules.films.service.swapi_client") as mock_client:
            mock_client._make_request = AsyncMock(return_value=response)

            result = await FilmService.search_films(search="1999")

            assert result["count"] == 2
