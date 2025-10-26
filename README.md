# System Design Challenges - 50 Projects

This repository contains 50 system design challenges organized into 10 weeks of learning. Each challenge includes a README with requirements, starter code with FastAPI, Docker configuration, and architecture notes.

## 🧭 Week 1–5: Requirements & Fundamentals

### Day 1: Instagram Feed Service (Functional Requirements Focus)
Design a minimal Instagram feed system (no full app) where users see posts from people they follow.
**Goal:** Extract and prioritize core functional requirements.

### Day 2: Global Weather Dashboard (Non-Functional Requirements Focus)
Build a weather app that must handle 1M users and 99.99% uptime.
**Goal:** Document latency, availability, and scalability metrics.

### Day 3: Feedback-Driven System Design Portal
Create a tool where users can submit design questions, and the system dynamically adjusts based on user feedback.
**Goal:** Show evolving requirements and trade-offs.

### Day 4: Requirements Analyzer CLI
Command-line app that classifies inputs into "functional" and "non-functional" using NLP.
**Goal:** Practice requirement parsing.

### Day 5: Scalable Requirements Tracker
Backend microservice to track and version evolving system requirements.
**Goal:** Manage changing specifications efficiently.

## ⚙️ Week 6–10: The Basics (Architecture, DB, Cache, Queue)

### Day 6: Client-Server Chat Application
Design a WebSocket-based chat with stateless backend servers and load balancing.
**Goal:** Demonstrate horizontal scaling.

### Day 7: Stateful Multiplayer Game Lobby System
Build a game lobby that keeps session data in-memory per server.
**Goal:** Understand stateful vs stateless trade-offs.

### Day 8: Database Migration Simulator
Visualize the pain of migrating from SQL → NoSQL (or vice versa).
**Goal:** CAP theorem + schema evolution.

### Day 9: Multi-Level Cache System
Implement API-level and DB-level caches (Redis + TTL + write-through).
**Goal:** Master cache invalidation policies.

### Day 10: Distributed Task Queue System
Build a message queue (RabbitMQ/Kafka clone-lite) for async jobs.
**Goal:** Handle load spikes gracefully.

## 🏗️ Week 11–15: Scaling & Trade-offs

### Day 11: Auto-Scaler Visualizer
Simulate vertical vs horizontal scaling with cost and latency graphs.
**Goal:** Learn when to scale up/out.

### Day 12: CAP Trade-Off Explorer
Interactive web tool where you toggle Consistency/Availability and see real-time effects.
**Goal:** CAP theorem in action.

### Day 13: High-Durability Payment Gateway
Build a small API that processes payments with guaranteed durability and transaction logs.
**Goal:** Explore Latency vs Durability.

### Day 14: Microservices vs Monolith Splitter
Convert a monolithic e-commerce app into microservices.
**Goal:** Analyze engineering cost vs independence.

### Day 15: Read vs Write Optimized Social App
Build a system where writes go to normalized DB, but reads hit denormalized cache.
**Goal:** Implement CQRS pattern.

## ⚖️ Week 16–20: Deep Trade-Off Applications

### Day 16: Strongly Consistent Auth System
Auth microservice ensuring immediate consistency after password resets.
**Goal:** Explore strong consistency design.

### Day 17: Eventually Consistent Social Feed
Feed updates propagate with delay but high availability.
**Goal:** Demonstrate eventual consistency.

### Day 18: Latency-Aware News App
Choose between caching, prefetching, or batching for lowest perceived latency.
**Goal:** Analyze UX vs backend trade-offs.

### Day 19: Durability-Optimized File Storage
Multi-replica storage system that prioritizes safety over speed.
**Goal:** Practice replication and WAL concepts.

### Day 20: Cost-Performance Optimizer
Build a dashboard that dynamically recommends cheaper configurations with minimal SLA impact.
**Goal:** Optimize engineering + cloud cost.

## 🧩 Week 21–25: Interview-Style End-to-End Designs

### Day 21: "Design Instagram" Simulator
Full design walk-through: feed, caching, scaling, failure planning.
**Goal:** Practice the 9-step design process.

### Day 22: Real-Time Analytics Pipeline
Design a system to collect, queue, and display live metrics (like Twitch or YouTube Analytics).
**Goal:** Integrate queues + scaling.

### Day 23: Event-Driven Order Processing System
Orders flow asynchronously across microservices via queues.
**Goal:** Handle async processing, retries, and DLQs.

### Day 24: Multi-Region Failover Simulation
Build a dashboard to test failover scenarios and latency effects.
**Goal:** Handle region outages and replication lag.

### Day 25: Monitoring & Observability Suite
Create logging, metrics, and alerting for any service.
**Goal:** Practice observability trade-offs.

## 💡 Week 26–30: Advanced, Research-Level Builds

### Day 26: Hybrid Strong + Eventual Consistency Platform
Combine both models within one system (e.g., social app with consistent login + eventual feeds).
**Goal:** Partition data based on consistency needs.

### Day 27: Dynamic Cache Invalidation AI Agent
AI service that predicts optimal cache TTLs.
**Goal:** Smart cache tuning.

### Day 28: AI-Powered Trade-Off Analyzer
LLM-based app that suggests trade-offs (CAP, cost, latency) from design input.
**Goal:** Combine AI + architecture reasoning.

### Day 29: Resilient Multi-Service Deployment Simulator
Kubernetes + chaos testing setup that measures recovery time under failures.
**Goal:** Failure handling and SLA tracking.

### Day 30: The "System Design Coach" App
A platform that asks system design questions and grades your diagrams + trade-off explanations.
**Goal:** Meta-project to master interviews.

## 🚀 Weeks 31-50: Advanced System Design Challenges

### Day 31: High-Throughput Logging Pipeline
Ingest, store, and query logs at scale.
**Goal:** Build efficient logging infrastructure.

### Day 32: Real-Time Collaboration Editor
OT/CRDT basics and sync strategies.
**Goal:** Implement collaborative editing features.

### Day 33: Geo-Distributed Key-Value Store
Consistency models and partitioning.
**Goal:** Design globally distributed storage.

### Day 34: Video Transcoding Service
Queueing, worker autoscaling, storage strategies.
**Goal:** Handle media processing at scale.

### Day 35: Recommendation Engine at Scale
Offline vs online model serving.
**Goal:** Build scalable recommendation systems.

### Day 36: Feature Flagging Service
Rollout strategies and targeting.
**Goal:** Implement safe feature deployments.

### Day 37: Search-as-a-Service Prototype
Index, shard, and query at scale.
**Goal:** Create a search platform.

### Day 38: Global Rate Limiter
Distributed token bucket implementation.
**Goal:** Protect services from overload.

### Day 39: Privacy-Preserving Analytics
Differential privacy basics.
**Goal:** Collect insights while protecting user privacy.

### Day 40: Federated Authentication Broker
Social auth + SSO across regions.
**Goal:** Implement secure authentication.

### Day 41: Edge-Cached CDN Prototype
Origin fallback and cache invalidation.
**Goal:** Build content delivery networks.

### Day 42: State Machine Workflow Engine
Durable workflow with retries.
**Goal:** Create reliable business processes.

### Day 43: Secure Audit Trail System
Tamper-evident logs and retention policies.
**Goal:** Maintain security compliance.

### Day 44: Graph-DB Based Social Graph
Friend recommendations and traversal.
**Goal:** Design social network infrastructure.

### Day 45: Massively Concurrent Websocket Hub
Scale connections efficiently.
**Goal:** Handle millions of concurrent users.

### Day 46: Time-Series Metrics Store
Ingestion, downsampling, retention policies.
**Goal:** Store and query time-series data.

### Day 47: Transactional Email Delivery Service
Retries, deliverability, and metrics.
**Goal:** Build reliable email systems.

### Day 48: Data Lake Ingestion Framework
Schema evolution and partitioning.
**Goal:** Process large-scale data.

### Day 49: Cost-Aware Autoscaler
Autoscale using cost + performance signals.
**Goal:** Optimize cloud resource usage.

### Day 50: Immutable Infrastructure Deployer
Infra as code with safe rollbacks.
**Goal:** Implement reliable deployments.