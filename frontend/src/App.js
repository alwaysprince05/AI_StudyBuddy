import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [topic, setTopic] = useState('');
  const [mathMode, setMathMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  // Load history and dark mode preference from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('studyHistory');
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
    setDarkMode(savedDarkMode);
  }, []);

  // Apply dark mode class
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const mode = mathMode ? 'math' : '';
      const response = await fetch(`${API_BASE_URL}/study?topic=${encodeURIComponent(topic)}&mode=${mode}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.error || 'Failed to fetch study materials';
        const errorDetails = errorData.details ? `\n\n${errorData.details}` : '';
        throw new Error(errorMessage + errorDetails);
      }

      const result = await response.json();
      setData(result);

      // Add to history
      const newHistory = [{ topic, timestamp: new Date().toISOString() }, ...history.slice(0, 9)];
      setHistory(newHistory);
      localStorage.setItem('studyHistory', JSON.stringify(newHistory));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadFromHistory = (historyTopic) => {
    setTopic(historyTopic);
  };

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <div className="container">
        <header className="header">
          <h1>🧠 Smart Study Assistant</h1>
          <p className="subtitle">AI-Powered Learning Companion</p>
          <button 
            className="dark-mode-toggle"
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </header>

        <form onSubmit={handleSubmit} className="search-form">
          <div className="input-group">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a study topic (e.g., Machine Learning, Calculus, Photosynthesis)"
              className="topic-input"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="submit-btn"
              disabled={loading || !topic.trim()}
            >
              {loading ? '⏳ Loading...' : '🚀 Study'}
            </button>
          </div>
          
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={mathMode}
              onChange={(e) => setMathMode(e.target.checked)}
              disabled={loading}
            />
            <span>Math Mode (Generate quantitative/logic questions)</span>
          </label>
        </form>

        {error && (
          <div className="error-message">
            <span>❌</span> 
            <div style={{ whiteSpace: 'pre-line' }}>{error}</div>
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Fetching data from Wikipedia and generating study materials...</p>
          </div>
        )}

        {data && !loading && (
          <div className="results-container">
            {data.mode === 'math' ? (
              <MathModeDisplay data={data} />
            ) : (
              <NormalModeDisplay data={data} />
            )}
          </div>
        )}

        {history.length > 0 && (
          <div className="history-section">
            <h3>📚 Recent Topics</h3>
            <div className="history-list">
              {history.map((item, idx) => (
                <button
                  key={idx}
                  className="history-item"
                  onClick={() => loadFromHistory(item.topic)}
                  disabled={loading}
                >
                  {item.topic}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function NormalModeDisplay({ data }) {
  return (
    <>
      <section className="result-section">
        <h2>📝 Summary</h2>
        <ul className="summary-list">
          {data.summary.map((point, idx) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </section>

      <section className="result-section">
        <h2>❓ Quiz</h2>
        <div className="quiz-container">
          {data.quiz.map((q, idx) => (
            <div key={idx} className="quiz-item">
              <h3>Question {idx + 1}</h3>
              <p className="question-text">{q.question}</p>
              <div className="options">
                {q.options.map((option, optIdx) => (
                  <div 
                    key={optIdx} 
                    className={`option ${String.fromCharCode(65 + optIdx) === q.correct ? 'correct' : ''}`}
                  >
                    <span className="option-label">{String.fromCharCode(65 + optIdx)}.</span>
                    {option}
                    {String.fromCharCode(65 + optIdx) === q.correct && (
                      <span className="correct-badge">✓ Correct</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="result-section">
        <h2>💡 Study Tip</h2>
        <p className="study-tip">{data.study_tip}</p>
      </section>
    </>
  );
}

function MathModeDisplay({ data }) {
  return (
    <>
      <section className="result-section">
        <h2>📝 Summary</h2>
        <ul className="summary-list">
          {data.summary && data.summary.map((point, idx) => (
            <li key={idx}>{point}</li>
          ))}
        </ul>
      </section>

      <section className="result-section">
        <h2>❓ Quiz</h2>
        <div className="quiz-container">
          {data.quiz && data.quiz.map((q, idx) => (
            <div key={idx} className="quiz-item">
              <h3>Question {idx + 1}</h3>
              <p className="question-text">{q.question}</p>
              <div className="options">
                {q.options.map((option, optIdx) => (
                  <div 
                    key={optIdx} 
                    className={`option ${String.fromCharCode(65 + optIdx) === q.correct ? 'correct' : ''}`}
                  >
                    <span className="option-label">{String.fromCharCode(65 + optIdx)}.</span>
                    {option}
                    {String.fromCharCode(65 + optIdx) === q.correct && (
                      <span className="correct-badge">✓ Correct</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="result-section">
        <h2>💡 Study Tip</h2>
        <p className="study-tip">{data.study_tip}</p>
      </section>

      <section className="result-section math-section">
        <h2>🔢 Math Question</h2>
        <div className="math-question">
          <h3>Question:</h3>
          <p className="question-text">{data.math_question.question}</p>
          
          <details className="answer-details">
            <summary>Show Answer</summary>
            <div className="answer-content">
              <h4>Answer:</h4>
              <p className="answer-text">{data.math_question.answer}</p>
              
              <h4>Explanation:</h4>
              <p className="explanation-text">{data.math_question.explanation}</p>
            </div>
          </details>
        </div>
      </section>
    </>
  );
}

export default App;
