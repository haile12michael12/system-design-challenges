.PHONY: help build run test unit-test integration-test performance-test clean logs shell

help:
	@echo "Available commands:"
	@echo "  build            - Build the Docker images"
	@echo "  run              - Start the services"
	@echo "  test             - Run all tests"
	@echo "  unit-test        - Run unit tests"
	@echo "  integration-test - Run integration tests"
	@echo "  performance-test - Run performance tests"
	@echo "  clean            - Stop and remove containers"
	@echo "  logs             - View service logs"
	@echo "  shell            - Open a shell in the API container"
	@echo "  migrate          - Run database migrations"
	@echo "  seed             - Seed database with test data"
	@echo "  seed-redis       - Seed Redis with test data"
	@echo "  benchmark        - Run benchmarks"
	@echo "  fake-data        - Generate fake data"

build:
	docker-compose build

run:
	docker-compose up -d

test:
	docker-compose run --rm api pytest

unit-test:
	docker-compose run --rm api pytest tests/unit

integration-test:
	docker-compose run --rm api pytest tests/integration

performance-test:
	docker-compose run --rm api python -m locust

clean:
	docker-compose down -v

logs:
	docker-compose logs -f

shell:
	docker-compose exec api /bin/bash

migrate:
	docker-compose run --rm api alembic upgrade head

seed:
	docker-compose run --rm api python scripts/seed_data.py

seed-redis:
	docker-compose run --rm api python scripts/seed_redis.py

benchmark:
	docker-compose run --rm api python scripts/benchmark_queries.py

fake-data:
	docker-compose run --rm api python scripts/generate_fake_data.py

dev:
	@echo "Starting development environment..."
	./scripts/bootstrap_local.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt[dev]