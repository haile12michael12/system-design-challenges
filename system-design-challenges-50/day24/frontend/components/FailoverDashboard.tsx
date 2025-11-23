'use client';

import React from 'react';

const FailoverDashboard = () => {
  // Mock data for regions
  const regions = [
    { id: 1, name: 'us-east-1', status: 'active', lag: 0.2, isPrimary: true },
    { id: 2, name: 'us-west-1', status: 'active', lag: 0.1, isPrimary: false },
    { id: 3, name: 'eu-central-1', status: 'lagging', lag: 5.2, isPrimary: false },
    { id: 4, name: 'ap-southeast-1', status: 'active', lag: 0.3, isPrimary: false },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-500';
      case 'lagging':
        return 'bg-yellow-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {regions.map((region) => (
        <div key={region.id} className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">{region.name}</h3>
              {region.isPrimary && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Primary
                </span>
              )}
            </div>
            <div className="mt-4 flex items-center">
              <div className={`flex-shrink-0 h-3 w-3 rounded-full ${getStatusColor(region.status)}`}></div>
              <div className="ml-2 text-sm text-gray-600 capitalize">{region.status}</div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              Lag: {region.lag}s
            </div>
            <div className="mt-4 flex space-x-2">
              <button className="text-xs bg-blue-500 hover:bg-blue-700 text-white py-1 px-2 rounded">
                Simulate Lag
              </button>
              <button className="text-xs bg-red-500 hover:bg-red-700 text-white py-1 px-2 rounded">
                Trigger Outage
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default FailoverDashboard;