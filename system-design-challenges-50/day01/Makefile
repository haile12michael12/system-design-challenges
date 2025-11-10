.PHONY: help run test lint format clean

help:
	@echo "Available commands:"
	@echo "  run     - Start the application"
	@echo "  test    - Run tests"
	@echo "  lint    - Run code linting"
	@echo "  format  - Format code"
	@echo "  clean   - Clean up temporary files"

run:
	uvicorn app.main:app --reload --port 8000

test:
	python -m pytest app/tests/ -v

lint:
	flake8 app/
	black --check app/

format:
	black app/
	isort app/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/