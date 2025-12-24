.PHONY: help install run test lint format clean

# -----------------------------
# Config
# -----------------------------
APP_MODULE=src.app.main:app
HOST=localhost
PORT=8000

# -----------------------------
# Help
# -----------------------------
help:
	@echo "Available commands:"
	@echo "  make install   Install dependencies"
	@echo "  make run       Run FastAPI app (dev)"
	@echo "  make test      Run tests"
	@echo "  make lint      Run linter"
	@echo "  make format    Format code"
	@echo "  make clean     Remove cache files"

# -----------------------------
# Install dependencies
# -----------------------------
install:
	poetry install

# -----------------------------
# Run application
# -----------------------------
run:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

# -----------------------------
# Tests
# -----------------------------
test:
	poetry run pytest

# -----------------------------
# Lint
# -----------------------------
lint:
	poetry run ruff check .

# -----------------------------
# Format
# -----------------------------
format:
	poetry run ruff format .

# -----------------------------
# Clean
# -----------------------------
clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -name "*.pyc" -delete
