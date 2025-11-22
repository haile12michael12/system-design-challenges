#!/bin/bash
# entrypoint.sh

# Exit on any error
set -e

# Activate virtual environment if it exists
if [ -f "/app/venv/bin/activate" ]; then
    source /app/venv/bin/activate
fi

# Wait for database to be ready
if [ "$WAIT_FOR_DB" = "true" ]; then
    echo "Waiting for database to be ready..."
    ./infra/scripts/wait-for-db.sh db:5432
fi

# Run migrations if requested
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Running database migrations..."
    alembic upgrade head
fi

# Execute the main command
echo "Starting application..."
exec "$@"