import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const startSimulation = async (config) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/cap/simulate`, {
      config: config,
      duration_seconds: 30
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to start simulation: ${error.message}`);
  }
};

export const getSimulationStatus = async (simulationId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/cap/simulation/${simulationId}`);
    return response.data;
  } catch (error) {
    throw new Error(`Failed to get simulation status: ${error.message}`);
  }
};