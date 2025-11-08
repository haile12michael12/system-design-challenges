#!/bin/bash
# Simple migration script wrapper

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

echo "Migrations completed!"