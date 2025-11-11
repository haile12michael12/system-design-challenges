"""
Tests for Autoscaler
"""
import pytest
from app.services.autoscaler import Autoscaler

def test_autoscaler_initialization():
    """Test autoscaler initialization"""
    autoscaler = Autoscaler()
    assert autoscaler.enabled == True
    assert autoscaler.target_cpu == 70.0
    assert autoscaler.min_replicas == 1
    assert autoscaler.max_replicas == 10
    assert autoscaler.current_replicas == 3

def test_scale_up():
    """Test scaling up"""
    autoscaler = Autoscaler()
    initial_replicas = autoscaler.current_replicas
    result = autoscaler.scale_up()
    assert autoscaler.current_replicas == initial_replicas + 1
    assert result["action"] == "scale_up"

def test_scale_down():
    """Test scaling down"""
    autoscaler = Autoscaler()
    initial_replicas = autoscaler.current_replicas
    result = autoscaler.scale_down()
    assert autoscaler.current_replicas == initial_replicas - 1
    assert result["action"] == "scale_down"

def test_cost_calculation():
    """Test cost calculation"""
    autoscaler = Autoscaler()
    cost = autoscaler.get_cost_per_hour()
    expected_cost = autoscaler.current_replicas * autoscaler.cost_per_replica_hour
    assert cost == expected_cost