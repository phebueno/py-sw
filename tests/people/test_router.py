from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from tests.factories.pagination import make_paginated
from tests.people.factories import make_person

from app.main import app

client = TestClient(app)


@patch("app.modules.people.router.PeopleService.search_people", new_callable=AsyncMock)
def test_list_people_adds_ids(mock_search_people):
    people = [make_person()]

    mock_search_people.return_value = make_paginated(people)

    response = client.get("/people?search=luke")

    assert response.status_code == 200
    assert response.json()["results"][0]["person_id"] == "1"


def test_list_people_invalid_page():
    response = client.get("/people?page=0")
    assert response.status_code == 422


@patch("app.modules.people.router.PeopleService.get_person", new_callable=AsyncMock)
def test_get_person_by_id(mock_get_person):
    mock_get_person.return_value = make_person()

    response = client.get("/people/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Luke Skywalker"
