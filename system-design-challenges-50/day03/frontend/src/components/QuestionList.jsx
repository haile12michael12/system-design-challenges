import React, { useState, useEffect } from 'react';
import { getQuestions } from '../api/questions';

const QuestionList = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const data = await getQuestions();
        setQuestions(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching questions:', error);
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  if (loading) {
    return <div>Loading questions...</div>;
  }

  return (
    <div>
      {questions.length === 0 ? (
        <p>No questions available.</p>
      ) : (
        <ul className="space-y-4">
          {questions.map((question) => (
            <li key={question.id} className="border p-4 rounded">
              <h3 className="font-semibold">{question.title}</h3>
              <p className="text-gray-600">{question.content}</p>
              <div className="mt-2 text-sm text-gray-500">
                Created: {new Date(question.created_at).toLocaleString()}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default QuestionList;