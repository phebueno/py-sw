.PHONY: dev serve start install

install:
	uv sync

dev:
	uv run -- fastapi dev app/main.py

serve:
	uv run -- uvicorn app.main:app --reload

start:
	uv run -- uvicorn app.main:app
