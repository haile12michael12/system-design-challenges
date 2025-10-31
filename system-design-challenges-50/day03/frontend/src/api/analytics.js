const API_BASE_URL = 'http://localhost:8000';

export const getAnalytics = async () => {
  const response = await fetch(`${API_BASE_URL}/analytics/`);
  if (!response.ok) {
    throw new Error('Failed to fetch analytics');
  }
  return response.json();
};

export const getQuestionAnalytics = async (questionId) => {
  const response = await fetch(`${API_BASE_URL}/analytics/${questionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch question analytics');
  }
  return response.json();
};

export const trackView = async (questionId) => {
  const response = await fetch(`${API_BASE_URL}/analytics/track-view/${questionId}`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to track view');
  }
  return response.json();
};

export const trackFeedback = async (questionId, rating) => {
  const response = await fetch(`${API_BASE_URL}/analytics/track-feedback/${questionId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ rating }),
  });
  if (!response.ok) {
    throw new Error('Failed to track feedback');
  }
  return response.json();
};