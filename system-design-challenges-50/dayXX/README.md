# Application Structure

This project follows a layered architecture pattern with clear separation of concerns.

## Directory Structure

```
app/
  api/
    routes/
    schemas/
  domain/
    entities/
    value_objects/
  application/
    commands/
    queries/
    handlers/
    events/
  infrastructure/
    db/
    cache/
    messaging/
    instrumentation/
  workers/
    tasks.py

tests/
  unit/
  integration/
```

## Components

### API Layer
- **routes**: API endpoint definitions
- **schemas**: Data validation schemas

### Domain Layer
- **entities**: Core business entities
- **value_objects**: Immutable value objects

### Application Layer
- **commands**: Command objects for write operations
- **queries**: Query objects for read operations
- **handlers**: Command and query handlers
- **events**: Domain events

### Infrastructure Layer
- **db**: Database implementations
- **cache**: Caching implementations
- **messaging**: Messaging implementations
- **instrumentation**: Monitoring and logging

### Workers
- **tasks.py**: Background task definitions

## Testing

- **unit**: Unit tests
- **integration**: Integration tests