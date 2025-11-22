# Makefile for Day 17 - Eventually Consistent Social Feed

# Variables
PYTHON := python3
PIP := pip
VENV := venv
DOCKER_COMPOSE := docker-compose

# Directories
INFRA_DIR := infra/compose
APP_DIR := app

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  docker-up   - Start all services with Docker Compose"
	@echo "  docker-down - Stop all services"
	@echo "  migrate     - Run database migrations"
	@echo "  worker      - Start Celery worker"
	@echo "  clean       - Clean Python cache files"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Run development server
.PHONY: dev
dev:
	$(PYTHON) -m uvicorn $(APP_DIR).main:app --reload --port 8000

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

# Start all services with Docker Compose
.PHONY: docker-up
docker-up:
	cd $(INFRA_DIR) && $(DOCKER_COMPOSE) up -d

# Stop all services
.PHONY: docker-down
docker-down:
	cd $(INFRA_DIR) && $(DOCKER_COMPOSE) down

# Run database migrations
.PHONY: migrate
migrate:
	$(PYTHON) -m alembic upgrade head

# Start Celery worker
.PHONY: worker
worker:
	$(PYTHON) -m celery -A $(APP_DIR).workers.celery_app worker --loglevel=info

# Clean Python cache files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

# Initialize development environment
.PHONY: init
init: install migrate

# Run all checks
.PHONY: check
check: test

# Run linter
.PHONY: lint
lint:
	$(PYTHON) -m flake8 $(APP_DIR) tests

# Run formatter
.PHONY: format
format:
	$(PYTHON) -m black $(APP_DIR) tests

# Generate migration
.PHONY: migration
migration:
	$(PYTHON) -m alembic revision --autogenerate -m "Auto migration"

# Show current database revision
.PHONY: current
current:
	$(PYTHON) -m alembic current