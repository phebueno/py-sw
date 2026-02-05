from app.modules.vehicles.schema import Vehicle


def make_vehicle(overrides: dict | None = None) -> dict:
    """Return a dict with default Vehicle data, optionally overridden."""
    data = Vehicle(
        name="Sand Crawler",
        model="Digger Crawler",
        manufacturer="Corellia Mining Corporation",
        cost_in_credits="150000",
        length="36.8",
        max_atmosphering_speed="30",
        crew="46",
        passengers="30",
        cargo_capacity="50000",
        consumables="2 months",
        vehicle_class="wheeled",
        pilots=[
            "https://swapi.dev/api/people/63/",
        ],
        films=[
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/5/",
        ],
        created="2014-12-10T15:36:25.724000Z",
        edited="2014-12-20T21:30:21.663000Z",
        url="https://swapi.dev/api/vehicles/4/",
    ).model_dump()

    if overrides:
        data.update(overrides)

    return data