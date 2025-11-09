#!/bin/bash
# Entrypoint script for the Docker container

# Exit on any error
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! pg_isready -h db -p 5432 -U postgres > /dev/null 2> /dev/null; do
    sleep 1
done

echo "Database is ready!"

# Initialize database tables
echo "Initializing database tables..."
python scripts/init_db.py

# Run any pending migrations
echo "Running database migrations..."
# alembic upgrade head

# Start the application
echo "Starting application..."
exec "$@"