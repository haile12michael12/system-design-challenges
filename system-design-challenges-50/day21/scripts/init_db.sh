#!/bin/bash

# Initialize database
echo "Initializing database..."

# Run database migrations
alembic upgrade head

# Create initial data
python -m scripts.seed_data

echo "Database initialization completed!"