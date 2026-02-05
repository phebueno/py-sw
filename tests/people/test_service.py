import respx
from httpx import Response
import pytest

from app.modules.people.service import PeopleService


@pytest.mark.asyncio
@respx.mock
async def test_search_people_without_search():
    respx.get(url__startswith="https://swapi.dev/api/people").mock(
        return_value=Response(
            200,
            json={
                "count": 1,
                "results": [{"name": "Luke Skywalker"}],
            },
        )
    )

    data = await PeopleService.search_people(page=1)

    assert data["count"] == 1
    assert data["results"][0]["name"] == "Luke Skywalker"


@pytest.mark.asyncio
@respx.mock
async def test_search_people_with_search():
    route = respx.get(url__startswith="https://swapi.dev/api/people").mock(
        return_value=Response(
            200,
            json={
                "count": 1,
                "results": [{"name": "Luke Skywalker"}],
            },
        )
    )

    data = await PeopleService.search_people(search="luke", page=1)

    assert route.called
    assert data["results"][0]["name"] == "Luke Skywalker"


@pytest.mark.asyncio
@respx.mock
async def test_get_person():
    respx.get("https://swapi.dev/api/people/1/").mock(
        return_value=Response(
            200,
            json={
                "name": "Luke Skywalker",
                "height": "172",
            },
        )
    )

    data = await PeopleService.get_person(person_id=1)

    assert data["name"] == "Luke Skywalker"
    assert data["height"] == "172"
