# System Architecture: Distributed File Storage System

## Overview

This document describes the architecture of the Distributed File Storage System, a durability-optimized storage solution with Write-Ahead Logging (WAL), replication, and recovery mechanisms.

## Design Goals

1. **Durability**: Ensure data persistence through WAL and replication
2. **Availability**: Maintain system availability through replication
3. **Scalability**: Support horizontal scaling of storage nodes
4. **Consistency**: Provide strong consistency through WAL replay and replica synchronization
5. **Observability**: Comprehensive metrics and tracing for monitoring and debugging

## System Components

### 1. Storage Layer

The storage layer consists of:
- **Primary Storage**: Main storage location for all files
- **Replica Storage**: Multiple replica locations for redundancy
- **Local Store**: Filesystem abstraction for local storage operations
- **Object Store**: Abstraction for cloud storage (S3/GCS)

### 2. Write-Ahead Log (WAL)

The WAL system ensures durability by logging all operations before execution:
- **WAL Service**: Manages WAL entries, checksums, and segment rotation
- **WAL Records**: Immutable log entries for each file operation
- **Segment Rotation**: Automatic rotation of WAL segments based on size
- **Checksums**: Data integrity verification for each WAL entry

### 3. Replication Service

Handles data replication across multiple nodes:
- **Synchronous Replication**: Immediate replication for critical operations
- **Asynchronous Replication**: Background replication using Celery workers
- **Replica Management**: Status monitoring and consistency checks
- **Failure Handling**: Graceful degradation when replicas are unavailable

### 4. Recovery Service

Manages system recovery and consistency:
- **Bootstrap**: System initialization and WAL replay on startup
- **WAL Replay**: Recovery of system state from WAL entries
- **Replica Recovery**: Recovery of primary storage from replicas
- **Consistency Validation**: Verification of data consistency across nodes

### 5. API Layer

RESTful API for file operations:
- **File Operations**: Upload, download, and delete endpoints
- **Health Checks**: System health and readiness endpoints
- **Admin Operations**: Replica inspection and WAL management
- **Authentication**: Security middleware for protected endpoints

### 6. Background Workers

Asynchronous task processing:
- **Replication Workers**: Handle asynchronous file replication
- **Periodic Tasks**: Regular consistency checks and maintenance
- **Task Queues**: Redis-based task queuing using Celery

### 7. Telemetry

Monitoring and observability:
- **Metrics**: Prometheus metrics for system performance
- **Tracing**: OpenTelemetry distributed tracing
- **Logging**: Structured JSON logging for debugging

## Data Flow

### File Upload

1. Client uploads file through API
2. File is stored in primary storage
3. WAL entry is created and persisted
4. Synchronous replication to all replicas
5. Asynchronous confirmation through Celery worker
6. Metrics updated and traces recorded

### File Download

1. Client requests file by ID
2. File retrieved from primary storage
3. Metrics updated and traces recorded
4. File content returned to client

### File Deletion

1. Client requests file deletion
2. File removed from primary storage
3. WAL entry created for deletion
4. Synchronous deletion from all replicas
5. Metrics updated and traces recorded

## WAL Implementation

### WAL Structure

```
WAL Segment (wal.segments/)
├── segment_1.wal
├── segment_2.wal
└── ...

Active WAL (wal.active)
```

### WAL Entry Format

Each WAL entry contains:
- **ID**: Unique identifier for the entry
- **Operation**: CREATE, UPDATE, or DELETE
- **File ID**: Identifier of the affected file
- **Data**: Serialized operation data
- **Checksum**: SHA256 checksum for data integrity
- **Segment ID**: Identifier of the containing segment
- **Position**: Position within the segment
- **Timestamp**: Creation timestamp

### Segment Rotation

Segments are rotated when they reach the configured size limit (default 1MB):
1. Active segment reaches size limit
2. Segment is closed and moved to segments directory
3. New active segment is created
4. WAL entries reference new segment

## Replication Strategy

### Synchronous Replication

For critical operations, data is replicated synchronously:
1. File operation executed on primary
2. Operation replicated to all replicas
3. Response returned only after all replicas confirm

### Asynchronous Replication

For non-critical operations, replication happens in background:
1. File operation executed on primary
2. Response returned immediately
3. Celery worker replicates to replicas
4. Replica status updated asynchronously

### Consistency Model

The system provides strong consistency through:
- WAL replay on startup
- Regular consistency checks
- Automatic repair mechanisms
- Replica synchronization

## Recovery Process

### System Bootstrap

On system startup:
1. Storage directories are initialized
2. WAL entries are replayed to recover state
3. Replicas are synchronized with primary
4. System is marked as ready for operations

### WAL Replay

To recover system state:
1. WAL entries are read in chronological order
2. Operations are applied to restore file state
3. Inconsistent files are removed or restored
4. System state is validated

### Replica Recovery

When primary storage is corrupted:
1. Healthy replica is selected as source
2. Primary storage is cleared
3. Files are copied from replica to primary
4. WAL is rebuilt from storage

## Scalability Considerations

### Horizontal Scaling

The system supports horizontal scaling through:
- **Storage Sharding**: Files distributed across multiple storage nodes
- **Replica Distribution**: Replicas spread across different availability zones
- **Load Balancing**: Requests distributed across multiple API instances

### Performance Optimization

Performance is optimized through:
- **Caching**: Frequently accessed files cached in memory
- **Batching**: Multiple operations batched for efficiency
- **Compression**: Files compressed before storage
- **Indexing**: Fast file lookup through indexing

## Fault Tolerance

### Failure Detection

The system detects failures through:
- **Health Checks**: Regular health checks for all components
- **Heartbeats**: Periodic heartbeats from replicas
- **Timeouts**: Operation timeouts for unresponsive components

### Failure Recovery

Recovery from failures is handled through:
- **Automatic Failover**: Switching to healthy replicas
- **Data Reconstruction**: Rebuilding lost data from WAL
- **Self-Healing**: Automatic repair of inconsistent replicas

## Security

### Data Protection

Data is protected through:
- **Encryption**: Files encrypted at rest and in transit
- **Access Control**: Role-based access control for operations
- **Audit Logging**: Comprehensive audit trail of all operations

### Authentication

Authentication is implemented through:
- **API Keys**: Token-based authentication for clients
- **JWT**: JSON Web Tokens for session management
- **OAuth**: Integration with OAuth providers

## Monitoring and Observability

### Metrics

Key metrics include:
- **Request Latency**: API response times
- **Throughput**: Number of operations per second
- **Error Rates**: Failed operation rates
- **Storage Usage**: Disk space utilization
- **Replica Lag**: Synchronization delays

### Tracing

Distributed tracing provides:
- **Request Flow**: End-to-end request tracking
- **Performance Bottlenecks**: Identification of slow operations
- **Error Propagation**: Tracking of error causes

### Logging

Structured logging includes:
- **Operation Logs**: Detailed logs of all file operations
- **System Logs**: Infrastructure and service logs
- **Security Logs**: Authentication and authorization events
- **Audit Logs**: Compliance and regulatory logs

## Deployment Architecture

### Containerization

The system is containerized using:
- **Docker**: Application containerization
- **Docker Compose**: Multi-container deployment
- **Kubernetes**: Orchestration for production deployments

### Service Dependencies

Required services include:
- **Database**: Metadata storage (SQLite/PostgreSQL)
- **Redis**: Task queue and caching
- **Load Balancer**: Traffic distribution
- **Monitoring**: Prometheus and Grafana

## Future Enhancements

### Planned Features

1. **Multi-Cloud Support**: Deployment across multiple cloud providers
2. **Advanced Compression**: Content-aware compression algorithms
3. **Machine Learning**: Predictive caching and optimization
4. **Advanced Security**: Homomorphic encryption and zero-knowledge storage
5. **Edge Computing**: Edge nodes for low-latency access

### Performance Improvements

1. **Parallel Processing**: Concurrent WAL processing
2. **Memory Mapping**: Direct memory access for large files
3. **Incremental Sync**: Delta synchronization for large files
4. **Smart Caching**: AI-driven caching strategies

## Conclusion

The Distributed File Storage System provides a robust, scalable, and durable solution for file storage needs. Through careful implementation of WAL, replication, and recovery mechanisms, the system ensures data persistence and availability while maintaining high performance and observability.