import { useState, useEffect } from 'react';
import { startSimulation, getSimulationResults } from '../services/api';

export const useSimulationFetcher = (simulationId) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getSimulationResults(simulationId);
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    if (simulationId) {
      fetchData();
    }
  }, [simulationId]);

  return { data, loading, error };
};