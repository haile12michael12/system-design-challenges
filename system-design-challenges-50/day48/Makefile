.PHONY: help build up down logs test clean install dev

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development commands
install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker commands
build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

logs-api: ## Show logs for API service
	docker-compose logs -f api

logs-worker: ## Show logs for worker service
	docker-compose logs -f worker

# Database commands
db-init: ## Initialize database
	docker-compose exec api python -c "from app.config.database import init_database; init_database()"

db-reset: ## Reset database (WARNING: This will delete all data)
	docker-compose down -v
	docker-compose up -d postgres
	sleep 10
	$(MAKE) db-init

# Testing commands
test: ## Run all tests
	pytest tests/ -v

test-unit: ## Run unit tests only
	pytest tests/unit/ -v

test-integration: ## Run integration tests only
	pytest tests/integration/ -v

test-coverage: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html --cov-report=term

# Code quality commands
lint: ## Run linting
	flake8 app/ tests/
	black --check app/ tests/
	mypy app/

format: ## Format code
	black app/ tests/
	isort app/ tests/

# Cleanup commands
clean: ## Clean up Docker resources
	docker-compose down -v
	docker system prune -f

clean-all: ## Clean up all Docker resources
	docker-compose down -v --rmi all
	docker system prune -af

# Monitoring commands
status: ## Show status of all services
	docker-compose ps

health: ## Check health of API service
	curl -f http://localhost:8000/health || echo "API is not healthy"

# Production commands
prod-build: ## Build production images
	docker build -t datalake-ingestion:latest .

prod-up: ## Start production services
	docker-compose -f docker-compose.prod.yml up -d

# Utility commands
shell-api: ## Open shell in API container
	docker-compose exec api /bin/bash

shell-db: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U postgres -d datalake

shell-redis: ## Open Redis shell
	docker-compose exec redis redis-cli

# Documentation
docs: ## Generate API documentation
	@echo "API documentation available at: http://localhost:8000/docs"
	@echo "ReDoc documentation available at: http://localhost:8000/redoc"

# Quick start
start: build up db-init ## Quick start: build, start services, and initialize database
	@echo "Services started! API available at: http://localhost:8000"
	@echo "API docs: http://localhost:8000/docs"
	@echo "MinIO console: http://localhost:9001 (minioadmin/minioadmin123)"
