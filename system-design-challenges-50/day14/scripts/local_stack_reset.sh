#!/bin/bash

# Reset the local development stack
echo "Resetting local development stack..."

# Stop and remove containers
echo "Stopping and removing containers..."
docker-compose -f ops/compose/docker-compose.dev.yml down

# Remove volumes
echo "Removing volumes..."
docker volume rm day14_postgres_data 2>/dev/null || true

# Remove networks
echo "Removing networks..."
docker network rm day14_ecommerce-network 2>/dev/null || true

# Clean up database files
echo "Cleaning up database files..."
rm -rf data/postgres 2>/dev/null || true

# Clean up Redis files
echo "Cleaning up Redis files..."
rm -rf data/redis 2>/dev/null || true

echo "Local development stack reset completed!"