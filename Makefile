.PHONY: dev serve start install

install:
	uv sync
	@echo "✅ Dependências instaladas!"

dev:
	uv run -- fastapi dev app/main.py

serve:
	uv run -- uvicorn app.main:app --reload

start:
	uv run -- uvicorn app.main:app

# Code Quality Commands
format:
	uv run isort app/
	uv run black app/
	@echo "✅ Código formatado!"

lint:
	uv run black --check app/
	uv run isort --check-only app/
	@echo "✅ Verificação completa!"

format-check:
	uv run isort --check-only app/
	uv run black --check app/
	@echo "✅ Nenhum erro de formatação!"

# Test Commands
test:
	uv run pytest -v
	@echo "✅ Testes concluídos!"

test-cov:
	uv run pytest --cov=app --cov-report=html
	@echo "✅ Cobertura gerada em htmlcov/index.html"

# Docker Commands
docker-build:
	docker build -t star-wars-api:latest .
	@echo "✅ Docker image built!"

docker-up:
	docker-compose up --build
	@echo "✅ Containers rodando!"

docker-down:
	docker-compose down
	@echo "✅ Containers parados!"

docker-logs:
	docker-compose logs -f

# Shortcuts/Aliases
build: docker-build
up: docker-up
down: docker-down
logs: docker-logs
test-all: test test-cov
quality: format lint test
