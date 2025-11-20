import React from 'react';

const AutoScaleControls = ({ instances, setInstances, workload, setWorkload }) => {
  const handleStartSimulation = () => {
    // In a real implementation, this would call the backend API
    console.log('Starting simulation with', instances, 'instances and', workload, 'workload');
  };

  return (
    <div className="autoscale-controls">
      <h2>Simulation Controls</h2>
      <div>
        <label>
          Instances:
          <input
            type="number"
            value={instances}
            onChange={(e) => setInstances(parseInt(e.target.value))}
            min="1"
          />
        </label>
      </div>
      <div>
        <label>
          Workload:
          <input
            type="number"
            value={workload}
            onChange={(e) => setWorkload(parseInt(e.target.value))}
            min="0"
          />
        </label>
      </div>
      <button onClick={handleStartSimulation}>Start Simulation</button>
    </div>
  );
};

export default AutoScaleControls;