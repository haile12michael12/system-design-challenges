# Makefile for common commands

# Variables
PYTHON = python3
PIP = pip
UVICORN = uvicorn
DOCKER_COMPOSE = docker-compose

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  run            - Run the application"
	@echo "  run-worker     - Run the worker"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  docker-up      - Start Docker containers"
	@echo "  docker-down    - Stop Docker containers"
	@echo "  seed-db        - Seed the database"
	@echo "  migrate        - Run database migrations"
	@echo "  load-test      - Run load test"

# Run the application
.PHONY: run
run:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

# Run the worker
.PHONY: run-worker
run-worker:
	$(PYTHON) -m app.workers.redis_worker

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest app/tests/ -v

# Run linting
.PHONY: lint
lint:
	@echo "Running black formatter..."
	black .
	@echo "Running flake8 linter..."
	flake8 .
	@echo "Running mypy type checker..."
	mypy .

# Start Docker containers
.PHONY: docker-up
docker-up:
	cd docker && $(DOCKER_COMPOSE) up --build

# Stop Docker containers
.PHONY: docker-down
docker-down:
	cd docker && $(DOCKER_COMPOSE) down

# Seed the database
.PHONY: seed-db
seed-db:
	$(PYTHON) scripts/seed_db.py

# Run database migrations
.PHONY: migrate
migrate:
	./scripts/migrate.sh

# Run load test
.PHONY: load-test
load-test:
	$(PYTHON) scripts/load_test.py