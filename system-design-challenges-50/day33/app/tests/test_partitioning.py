"""
Partitioning Tests
"""
import pytest
from app.core.hashing import ConsistentHasher

def test_consistent_hashing():
    """Test consistent hashing functionality"""
    nodes = ["us-east-1", "us-west-1", "eu-central-1"]
    hasher = ConsistentHasher(nodes)
    
    # Test that the same key always maps to the same node
    node1 = hasher.get_node("test_key")
    node2 = hasher.get_node("test_key")
    assert node1 == node2
    
    # Test that different keys can map to different nodes
    node3 = hasher.get_node("another_key")
    # This might be the same or different, but should be a valid node
    assert node3 in nodes

def test_add_node():
    """Test adding a node to the hash ring"""
    nodes = ["us-east-1", "us-west-1"]
    hasher = ConsistentHasher(nodes)
    
    # Add a new node
    hasher.add_node("eu-central-1")
    
    # Verify the new node is in the ring
    node = hasher.get_node("test_key")
    assert node in ["us-east-1", "us-west-1", "eu-central-1"]

def test_remove_node():
    """Test removing a node from the hash ring"""
    nodes = ["us-east-1", "us-west-1", "eu-central-1"]
    hasher = ConsistentHasher(nodes)
    
    # Remove a node
    hasher.remove_node("eu-central-1")
    
    # Verify the node is no longer in the ring
    node = hasher.get_node("test_key")
    assert node in ["us-east-1", "us-west-1"]