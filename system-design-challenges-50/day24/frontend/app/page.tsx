'use client';

import React from 'react';
import FailoverDashboard from '../components/FailoverDashboard';

export default function Home() {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-800">Dashboard Overview</h2>
        <div className="flex space-x-2">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Refresh
          </button>
          <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Trigger Failover
          </button>
        </div>
      </div>
      <FailoverDashboard />
    </div>
  );
}