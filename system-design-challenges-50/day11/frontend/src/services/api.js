import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const startSimulation = async (simulationData) => {
  try {
    const response = await api.post('/simulate', simulationData);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to start simulation: ${error.message}`);
  }
};

export const getSimulationResults = async (simulationId) => {
  try {
    const response = await api.get(`/simulate/${simulationId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch simulation results: ${error.message}`);
  }
};

export const getScalingRecommendation = async (currentInstances, workload) => {
  try {
    const response = await api.get('/autoscale/recommend', {
      params: { current_instances: currentInstances, workload }
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get scaling recommendation: ${error.message}`);
  }
};