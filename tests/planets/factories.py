from app.modules.planets.schema import Planet

def make_planet(overrides: dict | None = None) -> dict:
    """Return a dict with default Planet data, optionally overridden."""
    data = Planet(
        name="Tatooine",
        rotation_period="23",
        orbital_period="304",
        diameter="10465",
        climate="arid",
        gravity="1 standard",
        terrain="desert",
        surface_water="1",
        population="200000",
        residents=[],
        films=[],
        created="2014-12-09T13:50:49.641000Z",
        edited="2014-12-20T20:58:18.411000Z",
        url="https://swapi.dev/api/planets/1/",
    ).model_dump()

    if overrides:
        data.update(overrides)

    return data
