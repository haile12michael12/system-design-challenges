#!/bin/bash

# Pre-start script for the backend service

echo "Running pre-start script..."

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create initial data if needed
echo "Creating initial data..."
python app/db/init_db.py

echo "Pre-start script completed."