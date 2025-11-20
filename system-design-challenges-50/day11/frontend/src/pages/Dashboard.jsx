import React, { useEffect, useState } from 'react';
import { getSimulationResults } from '../services/api';
import GraphLatencyCost from '../components/GraphLatencyCost';
import InstanceVisualizer from '../components/InstanceVisualizer';

const Dashboard = () => {
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSimulationData = async () => {
      try {
        const data = await getSimulationResults('latest');
        setSimulationData(data);
      } catch (error) {
        console.error('Error fetching simulation data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSimulationData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Simulation Dashboard</h1>
      <GraphLatencyCost data={simulationData} />
      <InstanceVisualizer instances={simulationData?.instances || 0} />
    </div>
  );
};

export default Dashboard;