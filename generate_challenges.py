import os
import textwrap
import zipfile
from pathlib import Path

ROOT = Path("system-design-challenges-50")
if ROOT.exists():
    # remove existing to avoid duplicates
    import shutil
    shutil.rmtree(ROOT)

ROOT.mkdir(parents=True, exist_ok=True)

# Root README
root_readme = f"""# System Design Challenges — 50-Day Monorepo (Python + FastAPI + PostgreSQL)

This repository contains **50 system design challenge starters** (Day01 to Day50). Each folder contains:
- a short **README.md** describing the challenge, goals, and acceptance criteria
- a minimal **FastAPI** starter (`app/main.py`) and a `requirements.txt`
- a `Dockerfile` and `.env.sample`
- an architecture notes placeholder (`ARCHITECTURE.md`)
- instructions to run the minimal starter locally

**Assumptions made:** Tech stack is **Python + FastAPI + PostgreSQL**; templates are **Advanced** and **Learning-focused**.

## How to use this pack
1. Unzip the repository.
2. Pick a day folder (e.g., `day01`) and read its README for goals and constraints.
3. Create a Python virtualenv and install requirements: `pip install -r requirements.txt`
4. Run the starter app: `uvicorn app.main:app --reload --port 8000`
5. Extend the starter into a full prototype according to the README prompts.

---

This pack was generated automatically. Each day is scaffolded to help you focus on design rather than setup.
"""

(ROOT / "README.md").write_text(root_readme)

# Template contents for each day
for i in range(1, 51):
    day = f"day{str(i).zfill(2)}"
    day_path = ROOT / day
    src_path = day_path / "app"
    src_path.mkdir(parents=True, exist_ok=True)
    
    # README for the day (short description derived from earlier plan)
    # We'll craft a short mapping for the first 30 from earlier plan, then add 20 advanced extras.
    day_title = f"Day {i} - System Design Challenge"
    # Simple mapping for description (concise)
    descriptions = {
        1: "Instagram Feed (Functional Requirements Focus) - define core feed requirements and API contract.",
        2: "Weather Dashboard (Non-Functional Requirements Focus) - design for scale and 99.99% uptime.",
        3: "Requirements Analyzer CLI - parse functional vs non-functional requirements.",
        4: "Client-Server Chat App - basic WebSocket chat with load-balancer considerations.",
        5: "Stateful Multiplayer Lobby - session persistence and sticky connections.",
        6: "Database Migration Simulator - SQL <-> NoSQL trade-offs and migration plan.",
        7: "Reflection + Mini Review - document learnings and trade-offs.",
        8: "Multi-Level Cache System - API-level and DB-level caching strategies.",
        9: "Distributed Task Queue - implement producer/consumer pattern.",
        10: "Auto-Scaler Visualizer - vertical vs horizontal scaling simulation.",
        11: "CAP Trade-Off Explorer - interactive visualization of consistency vs availability.",
        12: "Latency-Aware News App - caching and prefetch strategies.",
        13: "Durability-Optimized File Store - replication and WAL techniques.",
        14: "Week Review: Scale Simulation - combine cache, queue, and scaling.",
        15: "Microservices vs Monolith Splitter - refactor a monolith into microservices.",
        16: "CQRS Social Feed - separate read/write paths for performance.",
        17: "Strongly Consistent Auth Service - immediate consistency for security-critical ops.",
        18: "Eventually Consistent Feed - availability-first feed system.",
        19: "Cost-Performance Optimizer - cloud cost vs performance dashboard.",
        20: "Multi-Region Failover Simulator - test region outages and failover.",
        21: "Resilience Review - trade-off summary and improvements.",
        22: "Real-Time Analytics Pipeline - stream processing and dashboards.",
        23: "Event-Driven Order Processing - async order lifecycle with DLQ.",
        24: "Monitoring & Observability Suite - metrics, tracing, alerts.",
        25: "Hybrid Consistency Platform - mix strong + eventual consistency.",
        26: "Dynamic Cache Invalidation AI Agent - predict TTLs with ML.",
        27: "AI-Powered Trade-Off Analyzer - LLM-assisted design recommendations.",
        28: "Resilient Multi-Service Deployment - chaos tests and K8s scenarios.",
        29: "System Design Coach App - grade design answers automatically.",
        30: "Capstone: Design a Global Platform - end-to-end design for a chosen product.",
    }
    # Add 20 advanced extras (31-50)
    extra_descs = {
        31: "High-Throughput Logging Pipeline - ingest, store, and query logs at scale.",
        32: "Real-Time Collaboration Editor - OT/CRDT basics and sync strategies.",
        33: "Geo-Distributed Key-Value Store - consistency models and partitioning.",
        34: "Video Transcoding Service - queueing, worker autoscaling, storage strategies.",
        35: "Recommendation Engine at Scale - offline vs online model serving.",
        36: "Feature Flagging Service - rollout strategies and targeting.",
        37: "Search-as-a-Service Prototype - index, shard, and query at scale.",
        38: "Global Rate Limiter - distributed token bucket implementation.",
        39: "Privacy-Preserving Analytics - differential privacy basics.",
        40: "Federated Authentication Broker - social auth + SSO across regions.",
        41: "Edge-Cached CDN Prototype - origin fallback and cache invalidation.",
        42: "State Machine Workflow Engine - durable workflow with retries.",
        43: "Secure Audit Trail System - tamper-evident logs and retention policies.",
        44: "Graph-DB Based Social Graph - friend recommendations and traversal.",
        45: "Massively Concurrent Websocket Hub - scale connections efficiently.",
        46: "Time-Series Metrics Store - ingestion, downsampling, retention policies.",
        47: "Transactional Email Delivery Service - retries, deliverability, and metrics.",
        48: "Data Lake Ingestion Framework - schema evolution and partitioning.",
        49: "Cost-Aware Autoscaler - autoscale using cost + performance signals.",
        50: "Immutable Infrastructure Deployer - infra as code with safe rollbacks.",
    }
    
    desc = descriptions.get(i, extra_descs.get(i, "System Design Challenge - expand this description in ARCHITECTURE.md"))
    
    readme_text = f"""# {day_title}\n\n**Summary:** {desc}\n\n## Learning Goals\n- Understand the core design trade-offs for this challenge.\n- Build a minimal prototype using FastAPI and Postgres-compatible patterns.\n- Add monitoring and failure scenarios where applicable.\n\n## Acceptance Criteria (suggested)\n- A runnable FastAPI starter in `app/main.py` that exposes a health endpoint.\n- `README.md` contains design prompts and next steps.\n- `ARCHITECTURE.md` stub with bullet points on components to design.\n\n## Quickstart (starter code)\n```bash\ncd {day}\npython -m venv .venv\nsource .venv/bin/activate  # or .venv\\Scripts\\activate on Windows\npip install -r requirements.txt\nuvicorn app.main:app --reload --port 8000\n```\n\n## Next steps (examples)\n- Expand the DB models in `app/db/models.py`.\n- Add caching with Redis.\n- Add a background worker using Celery or RQ.\n\n---\n"""

    (day_path / "README.md").write_text(readme_text)
    
    # ARCHITECTURE.md placeholder
    arch_text = f"# Architecture Notes — {day_title}\n\n- Components:\n  - API Gateway / Load Balancer\n  - FastAPI service(s)\n  - Postgres (or compatible) storage\n  - Cache (Redis)\n  - Worker queue (RabbitMQ / Redis Streams)\n\n- Suggested non-functional requirements:\n  - Target users / TPS:\n  - Latency targets:\n  - Availability SLA:\n\n- Failure scenarios to consider:\n  - DB partition\n  - Cache failure\n  - Worker backlog\n\n"
    (day_path / "ARCHITECTURE.md").write_text(arch_text)
    
    # app/main.py starter
    main_py = textwrap.dedent(f"""\
    from fastapi import FastAPI
    from pydantic import BaseModel
    
    app = FastAPI(title="{day_title}")
    
    class HealthResp(BaseModel):
        status: str = "ok"
    
    @app.get("/health", response_model=HealthResp)
    async def health():
        return HealthResp()
    
    @app.get("/hello")
    async def hello():
        return {{"message": "Hello from {day}"}}
    """)
    (src_path / "main.py").write_text(main_py)
    
    # basic db placeholder
    db_init = textwrap.dedent("""\
    # DB connection placeholder
    # Use asyncpg / databases / SQLAlchemy for Postgres connections in real projects.
    """)
    (src_path / "db.py").write_text(db_init)
    
    # requirements.txt
    requirements = "\n".join([
        "fastapi>=0.95.0",
        "uvicorn[standard]>=0.18.0",
        "pydantic>=1.10.0",
        "asyncpg>=0.26.0"
    ])
    (day_path / "requirements.txt").write_text(requirements)
    
    # Dockerfile
    dockerfile = textwrap.dedent("""\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
    """)
    (day_path / "Dockerfile").write_text(dockerfile)
    
    # .env.sample
    env_sample = "DATABASE_URL=postgresql://postgres:password@localhost:5432/dbname\nREDIS_URL=redis://localhost:6379/0\n"
    (day_path / ".env.sample").write_text(env_sample)
    
    # simple gitignore
    (day_path / ".gitignore").write_text(".venv\n__pycache__\n.env\n")
    
# create a simple root-level .gitignore
(ROOT / ".gitignore").write_text("**/__pycache__\n**/.venv\n*.pyc\n")

# Zip the directory
zip_path = Path("system-design-challenges-50.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for folder, _, files in os.walk(ROOT):
        for file in files:
            file_path = Path(folder) / file
            zf.write(file_path, file_path.relative_to(ROOT.parent))

print("Created zip:", zip_path)
zip_path_str = str(zip_path)
zip_path_str