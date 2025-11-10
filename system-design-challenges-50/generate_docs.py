#!/usr/bin/env python3
"""
Script to generate documentation for system design challenges
"""
import os
import sys
from pathlib import Path

def get_challenge_directories(base_path):
    """Get all challenge directories"""
    challenges = []
    for item in Path(base_path).iterdir():
        if item.is_dir() and item.name.startswith(('day', 'SystemDesign', 'High-Throughput')):
            challenges.append(item)
    return sorted(challenges, key=lambda x: x.name)

def check_existing_docs(challenge_path):
    """Check what documentation files already exist"""
    docs = {
        'README.md': (challenge_path / 'README.md').exists(),
        'ARCHITECTURE.md': (challenge_path / 'ARCHITECTURE.md').exists(),
        'docs_directory': (challenge_path / 'docs').exists(),
        'has_docker': (challenge_path / 'Dockerfile').exists(),
        'has_requirements': (challenge_path / 'requirements.txt').exists()
    }
    return docs

def generate_readme(challenge_path, challenge_name):
    """Generate README.md for a challenge"""
    readme_content = f"""# {challenge_name} - System Design Challenge

## Challenge Description
[Description of the challenge and its objectives]

## Learning Goals
- [Key concepts to understand]
- [Skills to develop]
- [System design principles to apply]

## Quickstart

### Prerequisites
- Python 3.9+
- Docker (optional but recommended)

### Using Docker (Recommended)
```bash
# Start all services
docker-compose up --build

# Stop all services
docker-compose down
```

### Local Development
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --port 8000
```

## Project Structure
```
{challenge_name}/
├── app/                    # Application code
├── tests/                  # Test files
├── README.md               # This file
├── ARCHITECTURE.md         # Architecture documentation
└── requirements.txt        # Python dependencies
```

## Testing
```bash
# Run unit tests
python -m pytest tests/
```

## Next Steps
- [Features to implement]
- [Improvements to consider]
"""
    
    with open(challenge_path / 'README.md', 'w') as f:
        f.write(readme_content)

def generate_architecture(challenge_path, challenge_name):
    """Generate ARCHITECTURE.md for a challenge"""
    arch_content = f"""# {challenge_name} - Architecture Documentation

## Overview
[High-level description of the system and its purpose]

## Core Components

### [Component Name]
- **Responsibility**: [What this component does]
- **Technology**: [Technology used]
- **Interfaces**: [How it communicates with other components]

## Technology Stack
- **Backend**: [Framework/language]
- **Database**: [Database technology]
- **Messaging**: [Queue/broker technology]
- **Caching**: [Cache technology]
- **Monitoring**: [Monitoring tools]

## Non-Functional Requirements

### Performance
- [Target throughput]
- [Latency requirements]

### Availability
- [Uptime targets]
- [Failover mechanisms]

### Scalability
- [Horizontal scaling capabilities]
- [Vertical scaling limits]

### Security
- [Authentication methods]
- [Authorization model]

## Design Patterns Used
### [Pattern Name]
[Description of how and why this pattern is used]

## Database Design
### Schema Overview
[Description of the database schema and relationships]

## API Design
### REST API
- [Endpoint structure]
- [Request/response formats]

## Monitoring and Observability
### Metrics
- [Key performance indicators]
- [System health metrics]

### Logging
- [Log structure]
- [Log levels]

## Security Implementation
### Authentication
- [Authentication flow]
- [Token management]

### Authorization
- [Access control model]
- [Permission management]

## Performance Optimization
### Database Optimization
- [Query optimization]
- [Connection pooling]

### Caching Optimization
- [Cache warming strategies]
- [Cache hit ratio monitoring]

## Future Considerations
### Short-term Improvements
- [Immediate enhancements]
- [Quick wins]

### Long-term Evolution
- [Architectural evolution plans]
- [Technology migration paths]

## Trade-offs
### [Decision]
- **Chosen Approach**: [Approach]
- **Alternative**: [Alternative]
- **Reasoning**: [Reasoning]
"""
    
    with open(challenge_path / 'ARCHITECTURE.md', 'w') as f:
        f.write(arch_content)

def main():
    """Main function to generate documentation for all challenges"""
    base_path = Path(__file__).parent
    challenges = get_challenge_directories(base_path)
    
    print(f"Found {len(challenges)} challenges")
    
    for challenge_path in challenges:
        challenge_name = challenge_path.name
        print(f"\nProcessing {challenge_name}...")
        
        # Check existing documentation
        docs_status = check_existing_docs(challenge_path)
        
        # Generate README.md if it doesn't exist
        if not docs_status['README.md']:
            print(f"  Creating README.md for {challenge_name}")
            generate_readme(challenge_path, challenge_name)
        else:
            print(f"  README.md already exists for {challenge_name}")
        
        # Generate ARCHITECTURE.md if it doesn't exist
        if not docs_status['ARCHITECTURE.md']:
            print(f"  Creating ARCHITECTURE.md for {challenge_name}")
            generate_architecture(challenge_path, challenge_name)
        else:
            print(f"  ARCHITECTURE.md already exists for {challenge_name}")
    
    print("\nDocumentation generation complete!")

if __name__ == "__main__":
    main()