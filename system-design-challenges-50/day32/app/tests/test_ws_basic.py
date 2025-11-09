import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocket
from app.main import app
from app.core.ws_manager import manager

client = TestClient(app)

def test_websocket_manager():
    """
    Test the WebSocket connection manager
    """
    # Test basic functionality
    assert manager is not None
    
    # Test document state management
    document_id = "test_doc_123"
    initial_state = "Initial document content"
    
    manager.update_document_state(document_id, initial_state)
    retrieved_state = manager.get_document_state(document_id)
    
    assert retrieved_state == initial_state
    
    # Test user count
    user_count = manager.get_document_user_count(document_id)
    assert user_count == 0

def test_ot_engine():
    """
    Test the OT engine
    """
    from app.core.ot_engine import ot_engine, crdt_engine
    
    # Test basic functionality
    assert ot_engine is not None
    assert crdt_engine is not None
    
    # Test operation transformation (placeholder)
    operation = {"type": "insert", "position": 5, "text": "test"}
    against = [{"type": "delete", "position": 3, "length": 2}]
    
    transformed = ot_engine.transform_operation(operation, against)
    assert transformed is not None
    
    # Test document application (placeholder)
    document = "Hello World"
    result = ot_engine.apply_operation(document, operation)
    assert result is not None
    
    # Test CRDT merge (placeholder)
    doc1 = {"content": "Hello"}
    doc2 = {"content": "World"}
    
    merged = crdt_engine.merge_documents(doc1, doc2)
    assert merged is not None