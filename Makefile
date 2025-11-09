.PHONY: help install format lint test test-cov clean

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pipenv install --dev
	pipenv run pip install -e .

format: ## Format code with ruff
	pipenv run ruff format .
	pipenv run ruff check --fix . || true

lint:  ## Run Ruff linter
	pipenv run ruff check .
	pipenv run ruff format --check .

type-check:  ## Run mypy type checker
	pipenv run mypy plugin.video.nhkworldtv/lib

test:  ## Run tests
	pipenv run pytest

test-cov:  ## Run tests with coverage report
	pipenv run pytest --cov=plugin.video.nhkworldtv/lib --cov-report=html --cov-report=term

test-watch:  ## Run tests in watch mode
	pipenv run pytest-watch

clean:  ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf .coverage
	rm -rf plugin.video.nhkworldtv-*.zip

all: format lint type-check test  ## Run format, lint, type-check, and test
