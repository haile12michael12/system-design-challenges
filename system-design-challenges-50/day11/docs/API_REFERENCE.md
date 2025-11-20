# API Reference - Auto-Scaler Visualizer

## Health Endpoints

### GET /api/v1/health
Health check endpoint to verify service availability.

**Response:**
```json
{
  "status": "healthy",
  "service": "autoscaler-backend"
}
```

## Simulation Endpoints

### POST /api/v1/simulate
Start a new simulation with specified parameters.

**Request Body:**
```json
{
  "instances": 2,
  "workload": 50,
  "scaling_type": "horizontal"
}
```

**Response:**
```json
{
  "simulation_id": "uuid-string",
  "status": "started"
}
```

### GET /api/v1/simulate/{simulation_id}
Get results for a specific simulation.

**Response:**
```json
{
  "simulation_id": "uuid-string",
  "status": "completed",
  "results": {
    "latency_data": [],
    "cost_data": [],
    "scaling_decisions": []
  }
}
```

## Autoscaling Endpoints

### GET /api/v1/autoscale/recommend
Get autoscaling recommendation based on current instances and workload.

**Query Parameters:**
- `current_instances` (integer): Number of current instances
- `workload` (integer): Current workload level

**Response:**
```json
{
  "timestamp": "timestamp",
  "action": "scale_up|scale_down|scale_out|scale_in|no_action",
  "reason": "Reason for the recommendation",
  "current_instances": 2,
  "new_instances": 3
}
```