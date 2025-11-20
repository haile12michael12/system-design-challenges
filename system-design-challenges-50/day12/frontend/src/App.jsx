import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

function App() {
  const [config, setConfig] = useState({
    consistency_level: 'strong',
    availability_level: 'high',
    partition_tolerance: true
  });
  
  const [simulation, setSimulation] = useState(null);
  const [simulationId, setSimulationId] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleStartSimulation = async () => {
    try {
      setIsRunning(true);
      const response = await axios.post(`${API_BASE_URL}/cap/simulate`, {
        config: config,
        duration_seconds: 30
      });
      
      setSimulationId(response.data.simulation_id);
      setSimulation(response.data);
    } catch (error) {
      console.error('Error starting simulation:', error);
      setIsRunning(false);
    }
  };

  const handleGetStatus = async () => {
    if (!simulationId) return;
    
    try {
      const response = await axios.get(`${API_BASE_URL}/cap/simulation/${simulationId}`);
      setSimulation(response.data);
      
      if (response.data.status === 'completed' || response.data.status === 'failed') {
        setIsRunning(false);
      }
    } catch (error) {
      console.error('Error getting simulation status:', error);
    }
  };

  useEffect(() => {
    let interval;
    if (isRunning && simulationId) {
      interval = setInterval(handleGetStatus, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning, simulationId]);

  return (
    <div className="App">
      <h1>CAP Theorem Visualizer</h1>
      
      <div>
        <h2>Configuration</h2>
        <div>
          <label>
            Consistency Level:
            <select 
              value={config.consistency_level} 
              onChange={(e) => setConfig({...config, consistency_level: e.target.value})}
            >
              <option value="strong">Strong</option>
              <option value="causal">Causal</option>
              <option value="eventual">Eventual</option>
            </select>
          </label>
        </div>
        
        <div>
          <label>
            Availability Level:
            <select 
              value={config.availability_level} 
              onChange={(e) => setConfig({...config, availability_level: e.target.value})}
            >
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </label>
        </div>
        
        <div>
          <label>
            Partition Tolerance:
            <input 
              type="checkbox" 
              checked={config.partition_tolerance} 
              onChange={(e) => setConfig({...config, partition_tolerance: e.target.checked})}
            />
          </label>
        </div>
        
        <button onClick={handleStartSimulation} disabled={isRunning}>
          {isRunning ? 'Running...' : 'Start Simulation'}
        </button>
      </div>
      
      {simulation && (
        <div>
          <h2>Simulation Results</h2>
          <p>Status: {simulation.status}</p>
          <p>Simulation ID: {simulation.simulation_id}</p>
          {simulation.states && simulation.states.length > 0 && (
            <div>
              <h3>Latest State</h3>
              <p>Consistency: {simulation.states[simulation.states.length - 1].consistency.toFixed(2)}</p>
              <p>Availability: {simulation.states[simulation.states.length - 1].availability.toFixed(2)}</p>
              <p>Partition Status: {simulation.states[simulation.states.length - 1].partition_status ? 'Active' : 'Inactive'}</p>
              <p>Latency: {simulation.states[simulation.states.length - 1].latency.toFixed(2)} ms</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;