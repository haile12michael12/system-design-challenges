.PHONY: install run test clean format check

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run the application
run:
	uvicorn app.main:app --reload --port 8000

# Run tests
test:
	pytest tests/ -v

# Clean Python cache files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/

# Format code
format:
	black .
	isort .

# Check code quality
check:
	flake8 .
	mypy .