from app.modules.starships.schema import Starship


def make_starship(overrides: dict | None = None) -> dict:
    """Return a dict with default Starship data, optionally overridden."""
    data = Starship(
        name="X-wing",
        model="T-65 X-wing starfighter",
        manufacturer="Incom Corporation",
        cost_in_credits="149999",
        length="12.9",
        max_atmosphering_speed="1050",
        crew="1",
        passengers="0",
        cargo_capacity="64",
        consumables="5 days",
        hyperdrive_rating="1.0",
        MGLT="100",
        starship_class="Starfighter",
        pilots=[
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/9/",
        ],
        films=[
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
            "https://swapi.dev/api/films/3/",
        ],
        created="2014-12-12T11:19:05.340000Z",
        edited="2014-12-20T21:23:49.886000Z",
        url="https://swapi.dev/api/starships/12/",
    ).model_dump()

    if overrides:
        data.update(overrides)

    return data