import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const GraphLatencyCost = ({ data }) => {
  // Mock data for demonstration
  const mockData = [
    { time: '0s', latency: 45, cost: 0.2 },
    { time: '10s', latency: 65, cost: 0.3 },
    { time: '20s', latency: 85, cost: 0.5 },
    { time: '30s', latency: 75, cost: 0.4 },
    { time: '40s', latency: 55, cost: 0.3 },
    { time: '50s', latency: 40, cost: 0.2 },
  ];

  const chartData = data || mockData;

  return (
    <div className="graph-latency-cost">
      <h2>Latency vs Cost</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="latency" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line yAxisId="right" type="monotone" dataKey="cost" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GraphLatencyCost;