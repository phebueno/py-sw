from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.modules.people.router import router as characters_router
from app.modules.films.router import router as films_router
from app.modules.planets.router import router as planets_router
from app.modules.species.router import router as species_router
from app.modules.starships.router import router as starships_router

from app.core.swapi_client import swapi_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando Star Wars API...")
    yield
    print("🛑 Encerrando Star Wars API...")
    await swapi_client.close()


app = FastAPI(
    title="Star Wars API",
    description="""
    API para explorar o universo Star Wars! 🌟
    
    Baseada na SWAPI (https://swapi.dev/), esta API oferece:
    - 🧑 Informações sobre personagens
    - 🪐 Dados sobre planetas
    - 🚀 Detalhes de naves espaciais
    - 🎬 Informações sobre os filmes
    
    ## Recursos Adicionais
    - Busca por nome
    - Paginação
    - Filtros avançados
    """,
    version="1.0.0",
    contact={"name": "Seu Nome", "email": "seu@email.com"},
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters_router, tags=["People"])
app.include_router(films_router, tags=["Films"])
app.include_router(planets_router, tags=["Planets"])
app.include_router(species_router, tags=["Species"])
app.include_router(starships_router, tags=["Starships"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"])
async def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "healthy", "service": "Star Wars API", "version": "1.0.0"}
