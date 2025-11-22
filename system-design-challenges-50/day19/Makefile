# Makefile for Day 19 - Distributed File Storage System

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

# Run tests
.PHONY: test
test:
	pytest tests/ -v

# Run tests with coverage
.PHONY: test-cov
test-cov:
	pytest tests/ --cov=app --cov-report=html

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
	celery -A app.workers.replicator_worker worker --loglevel=info

# Start Celery beat
.PHONY: beat
beat:
	celery -A app.workers.replicator_worker beat --loglevel=info

# Run load test
.PHONY: load-test
load-test:
	$(PYTHON) scripts/load_test.py

# Check replica consistency
.PHONY: check-replicas
check-replicas:
	$(PYTHON) scripts/repair_replicas.py --check-only

# Repair replicas
.PHONY: repair-replicas
repair-replicas:
	$(PYTHON) scripts/repair_replicas.py

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