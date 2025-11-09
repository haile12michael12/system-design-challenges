#!/usr/bin/env python3
"""
Seed the database with initial data
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.db.session import AsyncSessionLocal
from app.db.crud import DocumentCRUD
from app.db.models import Document

async def seed_data():
    """
    Seed the database with initial documents
    """
    print("Seeding database with initial data...")
    
    # Sample documents
    sample_documents = [
        {
            "title": "Project Plan",
            "content": "# Project Plan\n\n## Goals\n\n1. Implement real-time collaboration\n2. Add document versioning\n3. Ensure data consistency\n\n## Timeline\n\n- Week 1: Basic editor\n- Week 2: Collaboration features\n- Week 3: Testing and deployment",
            "owner_id": "user_1"
        },
        {
            "title": "Meeting Notes",
            "content": "# Team Meeting - 2025-11-09\n\n## Attendees\n- Alice\n- Bob\n- Charlie\n\n## Discussion Points\n\n1. Progress on document editor\n2. WebSocket implementation\n3. Database schema design\n\n## Action Items\n\n- Alice: Implement OT engine\n- Bob: Set up WebSocket connections\n- Charlie: Design database models",
            "owner_id": "user_2"
        },
        {
            "title": "Technical Documentation",
            "content": "# Technical Documentation\n\n## Architecture\n\nThe system uses:\n\n- FastAPI for the backend\n- WebSocket for real-time communication\n- PostgreSQL for data storage\n- Redis for caching\n\n## APIs\n\n### REST API\n\n- GET /documents - List documents\n- POST /documents - Create document\n- GET /documents/{id} - Get document\n- PUT /documents/{id} - Update document\n- DELETE /documents/{id} - Delete document\n\n### WebSocket API\n\n- /ws/editor/{document_id} - Collaborative editing",
            "owner_id": "user_1"
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for doc_data in sample_documents:
            document = await DocumentCRUD.create_document(
                db, 
                doc_data["title"], 
                doc_data["content"], 
                doc_data["owner_id"]
            )
            if document:
                print(f"Created document: {document.title} (ID: {document.id})")
            else:
                print(f"Failed to create document: {doc_data['title']}")
    
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_data())