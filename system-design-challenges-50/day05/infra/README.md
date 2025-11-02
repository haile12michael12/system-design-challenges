# Infrastructure

This directory contains infrastructure configuration files for deploying the Scalable Requirements Tracker application.

## Directory Structure

```
infra/
├── k8s/          # Kubernetes configuration files
├── env/          # Environment-specific configuration files
├── docker-compose.yml  # Docker Compose configuration
└── README.md     # This file
```

## Kubernetes Deployment

The application can be deployed to a Kubernetes cluster using the configuration files in the [k8s](k8s/) directory.

### Components

1. **Deployments**:
   - Backend deployment with 3 replicas
   - Frontend deployment with 3 replicas

2. **Services**:
   - Backend service (ClusterIP)
   - Frontend service (ClusterIP)
   - PostgreSQL service (ClusterIP)
   - Redis service (ClusterIP)

3. **Ingress**:
   - Ingress controller for routing external traffic

4. **ConfigMap**:
   - Configuration values for the application

5. **Secrets**:
   - Sensitive configuration values

6. **Horizontal Pod Autoscaler (HPA)**:
   - Automatic scaling based on CPU and memory usage

### Deployment Steps

1. Apply the configuration files in order:
   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml
   kubectl apply -f k8s/service-backend.yaml
   kubectl apply -f k8s/deployment-backend.yaml
   kubectl apply -f k8s/deployment-frontend.yaml
   kubectl apply -f k8s/ingress.yaml
   kubectl apply -f k8s/hpa.yaml
   ```

## Docker Compose

For local development and testing, you can use Docker Compose:

```bash
docker-compose up -d
```

This will start all services including:
- Backend API (FastAPI)
- Frontend (Vue.js)
- PostgreSQL database
- Redis cache
- Nginx reverse proxy

## Environment Configuration

Environment-specific configuration files are available in the [env](env/) directory:
- [.env.dev](env/.env.dev) - Development environment
- [.env.prod](env/.env.prod) - Production environment
- [.env.test](env/.env.test) - Test environment