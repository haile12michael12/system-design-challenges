import React, { useState, useEffect } from 'react';
import { getAnalytics } from '../api/analytics';

const AnalyticsChart = () => {
  const [analytics, setAnalytics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getAnalytics();
        setAnalytics(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching analytics:', error);
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div>Loading analytics...</div>;
  }

  return (
    <div>
      {analytics.length === 0 ? (
        <p>No analytics data available.</p>
      ) : (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded">
              <h3 className="font-semibold text-blue-800">Total Questions</h3>
              <p className="text-2xl">{analytics.length}</p>
            </div>
            <div className="bg-green-50 p-4 rounded">
              <h3 className="font-semibold text-green-800">Average Rating</h3>
              <p className="text-2xl">
                {(analytics.reduce((sum, item) => sum + item.avg_rating, 0) / analytics.length || 0).toFixed(2)}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded">
              <h3 className="font-semibold text-purple-800">Total Feedback</h3>
              <p className="text-2xl">
                {analytics.reduce((sum, item) => sum + item.total_feedback, 0)}
              </p>
            </div>
          </div>
          
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Question Analytics</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Question ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Views</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Rating</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feedback Count</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {analytics.map((item) => (
                    <tr key={item.question_id}>
                      <td className="px-6 py-4 whitespace-nowrap">{item.question_id}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{item.views}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{item.avg_rating.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{item.total_feedback}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyticsChart;