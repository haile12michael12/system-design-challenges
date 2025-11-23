#!/bin/bash

# Database migration script

set -e

echo "Starting database migration..."

# Check if we're running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    # Wait for database to be ready
    until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER; do
        echo "Waiting for database to be ready..."
        sleep 2
    done
else
    echo "Running locally"
    # Set default values for local development
    export DATABASE_HOST=${DATABASE_HOST:-localhost}
    export DATABASE_PORT=${DATABASE_PORT:-5432}
    export DATABASE_USER=${DATABASE_USER:-user}
    export DATABASE_NAME=${DATABASE_NAME:-feed_db}
fi

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

echo "Database migration completed successfully!"