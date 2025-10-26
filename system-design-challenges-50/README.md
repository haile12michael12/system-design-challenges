# System Design Challenges - 50 Projects

This repository contains 50 system design challenges organized into 10 weeks of learning. Each challenge includes a README with requirements, starter code with FastAPI, Docker configuration, and architecture notes.

## Tech Stack
- Python + FastAPI for backend services
- PostgreSQL for data persistence
- Docker for containerization
- Redis for caching (where applicable)
- RabbitMQ/Kafka for messaging (where applicable)

## Repository Structure
Each day's challenge is in its own folder (day01, day02, etc.) with:
- README.md - Challenge description and goals
- ARCHITECTURE.md - Architecture notes and design considerations
- app/main.py - Starter FastAPI application
- app/db.py - Database connection placeholder
- requirements.txt - Python dependencies
- Dockerfile - Container configuration
- .env.sample - Sample environment variables
- .gitignore - Git ignore rules

## Getting Started
1. Choose a day folder to work on
2. Read the README.md for challenge requirements
3. Create a Python virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `uvicorn app.main:app --reload --port 8000`
7. Access the API at http://localhost:8000

## Weeks Overview
- Weeks 1-5: Requirements & Fundamentals
- Weeks 6-10: The Basics (Architecture, DB, Cache, Queue)
- Weeks 11-15: Scaling & Trade-offs
- Weeks 16-20: Deep Trade-Off Applications
- Weeks 21-25: Interview-Style End-to-End Designs
- Weeks 26-30: Advanced, Research-Level Builds
- Weeks 31-50: Additional Advanced Challenges
