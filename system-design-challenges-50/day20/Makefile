# Makefile for Day 20 - Cost Optimization Recommendation Engine

# Variables
PYTHON := python3
PIP := pip
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Start development server"
	@echo "  test        - Run tests"
	@echo "  test-unit   - Run unit tests"
	@echo "  test-int    - Run integration tests"
	@echo "  docker-up   - Start services with Docker Compose"
	@echo "  docker-down - Stop services with Docker Compose"
	@echo "  clean       - Clean temporary files"
	@echo "  help        - Show this help message"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Start development server
.PHONY: dev
dev:
	$(PYTHON) app/main.py

# Run all tests
.PHONY: test
test:
	pytest tests/ -v

# Run unit tests
.PHONY: test-unit
test-unit:
	pytest tests/unit/ -v

# Run integration tests
.PHONY: test-int
test-int:
	pytest tests/integration/ -v

# Start services with Docker Compose
.PHONY: docker-up
docker-up:
	$(DOCKER_COMPOSE) up -d

# Stop services with Docker Compose
.PHONY: docker-down
docker-down:
	$(DOCKER_COMPOSE) down

# View logs
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Start Celery worker
.PHONY: worker
worker:
	celery -A app.workers.celery_app worker --loglevel=info

# Start Celery beat
.PHONY: beat
beat:
	celery -A app.workers.celery_app beat --loglevel=info

# Clean temporary files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Format code
.PHONY: format
format:
	black .
	isort .

# Lint code
.PHONY: lint
lint:
	flake8 .