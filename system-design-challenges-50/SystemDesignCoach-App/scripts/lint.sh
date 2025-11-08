#!/bin/bash
# Script to run code linting

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run linting tools
echo "Running black formatter..."
black .

echo "Running flake8 linter..."
flake8 .

echo "Running mypy type checker..."
mypy .

echo "Linting completed!"