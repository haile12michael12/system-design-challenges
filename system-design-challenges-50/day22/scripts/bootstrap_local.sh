#!/bin/bash

# Bootstrap script for local development environment

set -e

echo "🚀 Bootstrapping local development environment..."

# Check if we're on Windows (Git Bash) or Unix
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash
    IS_WINDOWS=1
else
    # Unix/Linux/Mac
    IS_WINDOWS=0
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.sample..."
    cp .env.sample .env
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ Error: pip not found. Please install Python and pip."
    exit 1
fi

# Initialize database
echo "Initializing database..."
if [ $IS_WINDOWS -eq 1 ]; then
    # Windows - use PowerShell
    powershell -Command "python scripts/init_db.py"
else
    # Unix/Linux/Mac
    python3 scripts/init_db.py
fi

# Start Docker services
echo "Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Run database migrations
echo "Running database migrations..."
if [ $IS_WINDOWS -eq 1 ]; then
    # Windows - use PowerShell
    powershell -Command "python -m alembic upgrade head"
else
    # Unix/Linux/Mac
    python3 -m alembic upgrade head
fi

# Seed database with test data
echo "Seeding database with test data..."
if [ $IS_WINDOWS -eq 1 ]; then
    # Windows - use PowerShell
    powershell -Command "python scripts/seed_data.py"
else
    # Unix/Linux/Mac
    python3 scripts/seed_data.py
fi

# Seed Redis with test data
echo "Seeding Redis with test data..."
if [ $IS_WINDOWS -eq 1 ]; then
    # Windows - use PowerShell
    powershell -Command "python scripts/seed_redis.py"
else
    # Unix/Linux/Mac
    python3 scripts/seed_redis.py
fi

echo "✅ Local development environment bootstrapped successfully!"
echo "🔧 Next steps:"
echo "   1. Start the development server: uvicorn app.main:app --reload"
echo "   2. Visit http://localhost:8000/docs for API documentation"
echo "   3. Run tests with: pytest"