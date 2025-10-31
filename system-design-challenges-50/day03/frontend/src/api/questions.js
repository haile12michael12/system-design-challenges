const API_BASE_URL = 'http://localhost:8000';

export const getQuestions = async () => {
  const response = await fetch(`${API_BASE_URL}/questions/`);
  if (!response.ok) {
    throw new Error('Failed to fetch questions');
  }
  return response.json();
};

export const getQuestion = async (id) => {
  const response = await fetch(`${API_BASE_URL}/questions/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch question');
  }
  return response.json();
};

export const createQuestion = async (questionData) => {
  const response = await fetch(`${API_BASE_URL}/questions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(questionData),
  });
  if (!response.ok) {
    throw new Error('Failed to create question');
  }
  return response.json();
};

export const submitFeedback = async (feedbackData) => {
  const response = await fetch(`${API_BASE_URL}/feedback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(feedbackData),
  });
  if (!response.ok) {
    throw new Error('Failed to submit feedback');
  }
  return response.json();
};

export const getFeedback = async (questionId) => {
  const response = await fetch(`${API_BASE_URL}/feedback/${questionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch feedback');
  }
  return response.json();
};