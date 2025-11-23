# Terraform Modules

This directory contains reusable Terraform modules for deploying the Feed Engine infrastructure.

## Modules

- **network** - VPC, subnets, and networking components
- **database** - PostgreSQL database setup
- **cache** - Redis cache setup
- **messaging** - Kafka messaging setup
- **compute** - ECS/EKS compute resources
- **monitoring** - Prometheus, Grafana, and OpenTelemetry setup

Each module is designed to be reusable and configurable for different environments.