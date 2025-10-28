# Makefile for Day 2 - Weather Dashboard

# Variables
PYTHON = python3
PIP = pip3
VENV = .venv
APP = app/main.py
TESTS = tests/

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  setup     - Set up the development environment"
	@echo "  run       - Run the application"
	@echo "  dev       - Run the application in development mode"
	@echo "  test      - Run tests"
	@echo "  docker    - Build and run with Docker"
	@echo "  compose   - Run with docker-compose"
	@echo "  clean     - Clean up generated files"
	@echo "  help      - Show this help message"

# Set up the development environment
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/Scripts/pip install -r requirements.txt

# Run the application
.PHONY: run
run:
	$(PYTHON) -m uvicorn $(APP):app --host 0.0.0.0 --port 8000

# Run the application in development mode
.PHONY: dev
dev:
	$(PYTHON) -m uvicorn $(APP):app --host 0.0.0.0 --port 8000 --reload

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TESTS) -v

# Build and run with Docker
.PHONY: docker
docker:
	docker build -t weather-dashboard .
	docker run -p 8000:8000 weather-dashboard

# Run with docker-compose
.PHONY: compose
compose:
	docker-compose up --build

# Clean up generated files
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Install development dependencies
.PHONY: install-dev
install-dev:
	$(PIP) install -r requirements-dev.txt

# Run linting
.PHONY: lint
lint:
	$(PYTHON) -m flake8 app/
	$(PYTHON) -m black --check app/
	$(PYTHON) -m mypy app/