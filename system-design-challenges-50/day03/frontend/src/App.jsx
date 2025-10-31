import React from 'react';
import QuestionList from './components/QuestionList';
import FeedbackForm from './components/FeedbackForm';
import AnalyticsChart from './components/AnalyticsChart';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Feedback-Driven System Design Portal
          </h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4">Questions</h2>
                <QuestionList />
              </div>
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4">Submit Feedback</h2>
                <FeedbackForm />
              </div>
            </div>
            <div className="mt-6 bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Analytics</h2>
              <AnalyticsChart />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;