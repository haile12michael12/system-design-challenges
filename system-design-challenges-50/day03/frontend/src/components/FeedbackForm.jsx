import React, { useState } from 'react';
import { submitFeedback } from '../api/questions';

const FeedbackForm = () => {
  const [formData, setFormData] = useState({
    question_id: '',
    rating: 5,
    comment: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage('');

    try {
      await submitFeedback(formData);
      setMessage('Feedback submitted successfully!');
      setFormData({
        question_id: '',
        rating: 5,
        comment: ''
      });
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setMessage('Error submitting feedback. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {message && (
        <div className={`p-2 rounded ${message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {message}
        </div>
      )}
      
      <div>
        <label htmlFor="question_id" className="block text-sm font-medium text-gray-700">
          Question ID
        </label>
        <input
          type="number"
          id="question_id"
          name="question_id"
          value={formData.question_id}
          onChange={handleChange}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>
      
      <div>
        <label htmlFor="rating" className="block text-sm font-medium text-gray-700">
          Rating (1-5)
        </label>
        <select
          id="rating"
          name="rating"
          value={formData.rating}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        >
          {[1, 2, 3, 4, 5].map(num => (
            <option key={num} value={num}>{num}</option>
          ))}
        </select>
      </div>
      
      <div>
        <label htmlFor="comment" className="block text-sm font-medium text-gray-700">
          Comment
        </label>
        <textarea
          id="comment"
          name="comment"
          value={formData.comment}
          onChange={handleChange}
          rows="3"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
        />
      </div>
      
      <button
        type="submit"
        disabled={submitting}
        className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
      >
        {submitting ? 'Submitting...' : 'Submit Feedback'}
      </button>
    </form>
  );
};

export default FeedbackForm;