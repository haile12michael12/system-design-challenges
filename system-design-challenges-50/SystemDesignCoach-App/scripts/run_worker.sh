#!/bin/bash
# Script to run the Celery worker

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Celery worker
celery -A app.workers.celery_app worker --loglevel=info