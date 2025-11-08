# Activity Selector - Makefile
# Works on both Windows (with make) and Ubuntu/Linux

.PHONY: help install run clean test format lint check dev

help:
	@echo "Activity Selector - Available Commands"
	@echo ""
	@echo "  make install    - Install dependencies with Poetry"
	@echo "  make run        - Run the application"
	@echo "  make clean      - Clean cache and temporary files"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with Black"
	@echo "  make lint       - Lint code with Flake8 and Pylint"
	@echo "  make check      - Run type checking with mypy"
	@echo "  make dev        - Install dev dependencies"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	poetry install --no-dev

run:
	@echo "🚀 Running Activity Selector..."
	poetry run python run.py

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

test:
	@echo "🧪 Running tests..."
	poetry run pytest

format:
	@echo "✨ Formatting code..."
	poetry run black .

lint:
	@echo "🔍 Linting code..."
	poetry run flake8 .
	poetry run pylint models services utils ui *.py

check:
	@echo "🔎 Type checking..."
	poetry run mypy .

dev:
	@echo "🛠️ Installing dev dependencies..."
	poetry install
