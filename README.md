Para dev:

```make dev```
OU
```uv run -- fastapi dev app/main.py```

Para build:
```
docker build -t star-wars-api:latest .
docker run -p 8000:8000 star-wars-api:latest
```

OU

```
docker-compose up --build
```