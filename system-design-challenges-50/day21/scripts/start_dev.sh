#!/bin/bash

# Start development environment
echo "Starting development environment..."

# Start Docker containers
docker-compose -f docker/docker-compose.dev.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Initialize database
echo "Initializing database..."
docker-compose -f docker/docker-compose.dev.yml exec app ./scripts/init_db.sh

echo "Development environment started!"
echo "API available at http://localhost:8000"