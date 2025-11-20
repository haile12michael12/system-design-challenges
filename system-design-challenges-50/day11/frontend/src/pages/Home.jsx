import React, { useState } from 'react';
import AutoScaleControls from '../components/AutoScaleControls';
import GraphLatencyCost from '../components/GraphLatencyCost';
import InstanceVisualizer from '../components/InstanceVisualizer';

const Home = () => {
  const [simulationData, setSimulationData] = useState(null);
  const [instances, setInstances] = useState(2);
  const [workload, setWorkload] = useState(50);

  return (
    <div className="home">
      <h1>Auto-Scaler Visualizer</h1>
      <div className="content">
        <AutoScaleControls 
          instances={instances}
          setInstances={setInstances}
          workload={workload}
          setWorkload={setWorkload}
        />
        <GraphLatencyCost data={simulationData} />
        <InstanceVisualizer instances={instances} />
      </div>
    </div>
  );
};

export default Home;