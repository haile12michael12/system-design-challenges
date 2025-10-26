import os
import textwrap
import zipfile
from pathlib import Path

# Project descriptions organized by weeks
descriptions = {
    1: "Instagram Feed (Functional Requirements Focus) - Design a minimal Instagram feed system (no full app) where users see posts from people they follow. Goal: Extract and prioritize core functional requirements.",
    2: "Weather Dashboard (Non-Functional Requirements Focus) - Build a weather app that must handle 1M users and 99.99% uptime. Goal: Document latency, availability, and scalability metrics.",
    3: "Feedback-Driven System Design Portal - Create a tool where users can submit design questions, and the system dynamically adjusts based on user feedback. Goal: Show evolving requirements and trade-offs.",
    4: "Requirements Analyzer CLI - Command-line app that classifies inputs into 'functional' and 'non-functional' using NLP. Goal: Practice requirement parsing.",
    5: "Scalable Requirements Tracker - Backend microservice to track and version evolving system requirements. Goal: Manage changing specifications efficiently.",
    6: "Client-Server Chat Application - Design a WebSocket-based chat with stateless backend servers and load balancing. Goal: Demonstrate horizontal scaling.",
    7: "Stateful Multiplayer Game Lobby System - Build a game lobby that keeps session data in-memory per server. Goal: Understand stateful vs stateless trade-offs.",
    8: "Database Migration Simulator - Visualize the pain of migrating from SQL to NoSQL (or vice versa). Goal: CAP theorem + schema evolution.",
    9: "Multi-Level Cache System - Implement API-level and DB-level caches (Redis + TTL + write-through). Goal: Master cache invalidation policies.",
    10: "Distributed Task Queue System - Build a message queue (RabbitMQ/Kafka clone-lite) for async jobs. Goal: Handle load spikes gracefully.",
    11: "Auto-Scaler Visualizer - Simulate vertical vs horizontal scaling with cost and latency graphs. Goal: Learn when to scale up/out.",
    12: "CAP Trade-Off Explorer - Interactive web tool where you toggle Consistency/Availability and see real-time effects. Goal: CAP theorem in action.",
    13: "High-Durability Payment Gateway - Build a small API that processes payments with guaranteed durability and transaction logs. Goal: Explore Latency vs Durability.",
    14: "Microservices vs Monolith Splitter - Convert a monolithic e-commerce app into microservices. Goal: Analyze engineering cost vs independence.",
    15: "Read vs Write Optimized Social App - Build a system where writes go to normalized DB, but reads hit denormalized cache. Goal: Implement CQRS pattern.",
    16: "Strongly Consistent Auth System - Auth microservice ensuring immediate consistency after password resets. Goal: Explore strong consistency design.",
    17: "Eventually Consistent Social Feed - Feed updates propagate with delay but high availability. Goal: Demonstrate eventual consistency.",
    18: "Latency-Aware News App - Choose between caching, prefetching, or batching for lowest perceived latency. Goal: Analyze UX vs backend trade-offs.",
    19: "Durability-Optimized File Storage - Multi-replica storage system that prioritizes safety over speed. Goal: Practice replication and WAL concepts.",
    20: "Cost-Performance Optimizer - Build a dashboard that dynamically recommends cheaper configurations with minimal SLA impact. Goal: Optimize engineering + cloud cost.",
    21: "Design Instagram Simulator - Full design walk-through: feed, caching, scaling, failure planning. Goal: Practice the 9-step design process.",
    22: "Real-Time Analytics Pipeline - Design a system to collect, queue, and display live metrics (like Twitch or YouTube Analytics). Goal: Integrate queues + scaling.",
    23: "Event-Driven Order Processing System - Orders flow asynchronously across microservices via queues. Goal: Handle async processing, retries, and DLQs.",
    24: "Multi-Region Failover Simulation - Build a dashboard to test failover scenarios and latency effects. Goal: Handle region outages and replication lag.",
    25: "Monitoring & Observability Suite - Create logging, metrics, and alerting for any service. Goal: Practice observability trade-offs.",
    26: "Hybrid Strong + Eventual Consistency Platform - Combine both models within one system (e.g., social app with consistent login + eventual feeds). Goal: Partition data based on consistency needs.",
    27: "Dynamic Cache Invalidation AI Agent - AI service that predicts optimal cache TTLs. Goal: Smart cache tuning.",
    28: "AI-Powered Trade-Off Analyzer - LLM-based app that suggests trade-offs (CAP, cost, latency) from design input. Goal: Combine AI + architecture reasoning.",
    29: "Resilient Multi-Service Deployment Simulator - Kubernetes + chaos testing setup that measures recovery time under failures. Goal: Failure handling and SLA tracking.",
    30: "System Design Coach App - A platform that asks system design questions and grades your diagrams + trade-off explanations. Goal: Meta-project to master interviews.",
}

# Additional advanced challenges (31-50)
extra_descs = {
    31: "High-Throughput Logging Pipeline - Ingest, store, and query logs at scale. Goal: Build efficient logging infrastructure.",
    32: "Real-Time Collaboration Editor - OT/CRDT basics and sync strategies. Goal: Implement collaborative editing features.",
    33: "Geo-Distributed Key-Value Store - Consistency models and partitioning. Goal: Design globally distributed storage.",
    34: "Video Transcoding Service - Queueing, worker autoscaling, storage strategies. Goal: Handle media processing at scale.",
    35: "Recommendation Engine at Scale - Offline vs online model serving. Goal: Build scalable recommendation systems.",
    36: "Feature Flagging Service - Rollout strategies and targeting. Goal: Implement safe feature deployments.",
    37: "Search-as-a-Service Prototype - Index, shard, and query at scale. Goal: Create a search platform.",
    38: "Global Rate Limiter - Distributed token bucket implementation. Goal: Protect services from overload.",
    39: "Privacy-Preserving Analytics - Differential privacy basics. Goal: Collect insights while protecting user privacy.",
    40: "Federated Authentication Broker - Social auth + SSO across regions. Goal: Implement secure authentication.",
    41: "Edge-Cached CDN Prototype - Origin fallback and cache invalidation. Goal: Build content delivery networks.",
    42: "State Machine Workflow Engine - Durable workflow with retries. Goal: Create reliable business processes.",
    43: "Secure Audit Trail System - Tamper-evident logs and retention policies. Goal: Maintain security compliance.",
    44: "Graph-DB Based Social Graph - Friend recommendations and traversal. Goal: Design social network infrastructure.",
    45: "Massively Concurrent Websocket Hub - Scale connections efficiently. Goal: Handle millions of concurrent users.",
    46: "Time-Series Metrics Store - Ingestion, downsampling, retention policies. Goal: Store and query time-series data.",
    47: "Transactional Email Delivery Service - Retries, deliverability, and metrics. Goal: Build reliable email systems.",
    48: "Data Lake Ingestion Framework - Schema evolution and partitioning. Goal: Process large-scale data.",
    49: "Cost-Aware Autoscaler - Autoscale using cost + performance signals. Goal: Optimize cloud resource usage.",
    50: "Immutable Infrastructure Deployer - Infra as code with safe rollbacks. Goal: Implement reliable deployments.",
}

# Create root directory
ROOT = Path("system-design-challenges-50")
if ROOT.exists():
    import shutil
    shutil.rmtree(ROOT)

ROOT.mkdir(parents=True, exist_ok=True)

# Create root README
root_readme = """# System Design Challenges - 50 Projects

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
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\\Scripts\\activate` (Windows)
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
"""

(ROOT / "README.md").write_text(root_readme, encoding='utf-8')

# Create .gitignore
gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
ENV/

# Environment variables
.env

# IDE
.vscode/
.idea/

# Docker
*.log
"""
(ROOT / ".gitignore").write_text(gitignore_content, encoding='utf-8')

# Generate folders for each day
for i in range(1, 51):
    day = f"day{str(i).zfill(2)}"
    day_path = ROOT / day
    src_path = day_path / "app"
    src_path.mkdir(parents=True, exist_ok=True)
    
    # Get description
    desc = descriptions.get(i, extra_descs.get(i, "System Design Challenge"))
    day_title = f"Day {i} - {desc.split(' - ')[0]}"
    
    # Create README.md for the day
    readme_text = f"""# {day_title}

## Challenge Description
{desc}

## Learning Goals
- Understand the core design trade-offs for this challenge
- Build a minimal prototype using FastAPI and Postgres-compatible patterns
- Add monitoring and failure scenarios where applicable

## Acceptance Criteria
- A runnable FastAPI starter in `app/main.py` that exposes a health endpoint
- `README.md` contains design prompts and next steps
- `ARCHITECTURE.md` with bullet points on components to design
- Dockerfile for containerization
- requirements.txt with dependencies

## Quickstart
```bash
cd {day}
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Next Steps
- Expand the DB models in `app/db/models.py`
- Add caching with Redis where applicable
- Add a background worker using Celery or RQ
- Implement proper error handling and validation
- Add unit and integration tests
"""

    (day_path / "README.md").write_text(readme_text, encoding='utf-8')
    
    # Create ARCHITECTURE.md
    arch_text = f"""# Architecture Notes - {day_title}

## Components to Consider
- API Gateway / Load Balancer
- FastAPI service(s)
- Postgres (or compatible) storage
- Cache (Redis)
- Worker queue (RabbitMQ / Redis Streams)
- Monitoring and logging stack

## Suggested Non-Functional Requirements
- Target users / TPS:
- Latency targets:
- Availability SLA:
- Data durability requirements:
- Security considerations:

## Failure Scenarios to Consider
- DB partition
- Cache failure
- Worker backlog
- Network latency
- Service degradation

## Scalability Considerations
- Horizontal vs vertical scaling
- Database sharding strategy
- Caching strategy
- Load balancing approach
- CDN requirements

## Technology Choices
- Justify your choice of database (SQL vs NoSQL)
- Explain caching strategy
- Describe queueing mechanism
- Outline monitoring approach
"""

    (day_path / "ARCHITECTURE.md").write_text(arch_text, encoding='utf-8')
    
    # Create app/main.py
    main_py = textwrap.dedent(f"""\
    from fastapi import FastAPI
    from pydantic import BaseModel
    
    app = FastAPI(title="{day_title}")
    
    class HealthResp(BaseModel):
        status: str = "ok"
        service: str = "{day}"
    
    @app.get("/health", response_model=HealthResp)
    async def health():
        return HealthResp()
    
    @app.get("/")
    async def root():
        return {{"message": "Welcome to {day_title}"}}
    
    @app.get("/hello")
    async def hello():
        return {{"message": "Hello from {day}"}}
    """)
    (src_path / "main.py").write_text(main_py, encoding='utf-8')
    
    # Create app/db.py
    db_init = textwrap.dedent("""\
    # DB connection placeholder
    # Use asyncpg / databases / SQLAlchemy for Postgres connections in real projects.
    
    # Example:
    # import asyncpg
    # import os
    #
    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/dbname")
    #
    # async def get_db_connection():
    #     conn = await asyncpg.connect(DATABASE_URL)
    #     return conn
    """)
    (src_path / "db.py").write_text(db_init, encoding='utf-8')
    
    # Create requirements.txt
    requirements = "\n".join([
        "fastapi>=0.95.0",
        "uvicorn[standard]>=0.18.0",
        "pydantic>=1.10.0",
        "asyncpg>=0.26.0"
    ])
    (day_path / "requirements.txt").write_text(requirements, encoding='utf-8')
    
    # Create Dockerfile
    dockerfile = textwrap.dedent("""\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    EXPOSE 8000
    CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
    """)
    (day_path / "Dockerfile").write_text(dockerfile, encoding='utf-8')
    
    # Create .env.sample
    env_sample = "DATABASE_URL=postgresql://postgres:password@localhost:5432/dbname\nREDIS_URL=redis://localhost:6379/0\n"
    (day_path / ".env.sample").write_text(env_sample, encoding='utf-8')
    
    # Create .gitignore for day folder
    (day_path / ".gitignore").write_text(".venv\n__pycache__\n.env\n*.log", encoding='utf-8')

# Zip the directory
zip_path = Path("system-design-challenges-50.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for folder, _, files in os.walk(ROOT):
        for file in files:
            file_path = Path(folder) / file
            zf.write(file_path, file_path.relative_to(ROOT.parent))

print(f"Created zip: {zip_path}")