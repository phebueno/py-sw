from app.modules.species.schema import Species


def make_species(overrides: dict | None = None) -> dict:
    """Return a dict with default Species data, optionally overridden."""
    data = Species(
        name="Human",
        classification="mammal",
        designation="sentient",
        average_height="180",
        skin_colors="caucasian, black, asian, hispanic",
        hair_colors="blonde, brown, black, red",
        eye_colors="brown, blue, green, hazel",
        average_lifespan="120",
        homeworld="https://swapi.dev/api/planets/9/",
        language="Galactic Basic",
        people=[
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/5/",
        ],
        films=[
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/",
        ],
        created="2014-12-10T13:52:11.567000Z",
        edited="2014-12-20T21:36:42.136000Z",
        url="https://swapi.dev/api/species/1/",
    ).model_dump()

    if overrides:
        data.update(overrides)

    return data