import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jargonAPI } from '../utils/api';
import '../App.css';

function JargonBuster({ darkMode, setDarkMode }) {
  const [search, setSearch] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [recentSearches, setRecentSearches] = useState([]);
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  // Popular medical terms for quick access
  const popularTerms = [
    { term: 'Hemoglobin', icon: '🩸', category: 'Blood' },
    { term: 'Cholesterol', icon: '❤️', category: 'Heart' },
    { term: 'Glucose', icon: '🍬', category: 'Blood Sugar' },
    { term: 'Hypertension', icon: '📈', category: 'Blood Pressure' },
    { term: 'Anemia', icon: '🔴', category: 'Blood' },
    { term: 'Diabetes', icon: '💉', category: 'Metabolic' },
    { term: 'Thyroid', icon: '🦋', category: 'Endocrine' },
    { term: 'Creatinine', icon: '🫘', category: 'Kidney' },
  ];

  const explainTerm = async (termToExplain = null) => {
    const searchTerm = termToExplain || search.trim();
    
    if (!searchTerm) {
      setError('Please enter a medical term');
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await jargonAPI.explain(searchTerm);
      setResult(res.data);
      
      // Add to recent searches (limit to 5)
      setRecentSearches(prev => {
        const updated = [searchTerm, ...prev.filter(t => t !== searchTerm)].slice(0, 5);
        return updated;
      });
      
      setSearch('');
    } catch (err) {
      console.error('Jargon API error:', err);
      setError(err.response?.data?.error || 'Could not explain term. Try another.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className="dashboard-wrapper">
      {/* Modern Navbar */}
      <nav className="modern-navbar">
        <div className="navbar-content">
          <div className="navbar-logo" onClick={() => navigate('/dashboard')}>
            <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="#2563EB"/>
              <rect x="14" y="10" width="20" height="28" rx="2" fill="white"/>
              <line x1="18" y1="16" x2="30" y2="16" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <line x1="18" y1="20" x2="30" y2="20" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <line x1="18" y1="24" x2="26" y2="24" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
              <circle cx="24" cy="31" r="4" fill="#2563EB"/>
              <path d="M24 29v4M22 31h4" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <span className="navbar-brand">MedLens</span>
          </div>

          <div className="navbar-links">
            <a href="/dashboard" className="nav-link">Dashboard</a>
            <a href="/history" className="nav-link">History</a>
            <a href="/health" className="nav-link">Analytics</a>
          </div>

          <div className="navbar-right">
            <button onClick={toggleDarkMode} className="icon-button">
              {darkMode ? (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
                </svg>
              )}
            </button>
            
            <button onClick={handleLogout} className="navbar-logout-btn">
              Logout
            </button>
            
            <div className="navbar-profile">
              <div className="profile-avatar">
                {username?.charAt(0).toUpperCase()}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="jargon-container">
        {/* Hero Section with Search */}
        <div className="jargon-hero">
          <div className="jargon-hero-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h1>Medical Jargon Buster</h1>
          <p>Understand any medical term in simple language</p>

          {/* Search Bar */}
          <div className="jargon-search-wrapper">
            <svg className="search-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd"/>
            </svg>
            <input
              type="text"
              className="jargon-search-input"
              placeholder="Enter medical term (e.g., hemoglobin, cholesterol)"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && explainTerm()}
            />
            <button
              onClick={() => explainTerm()}
              disabled={loading}
              className="jargon-search-btn"
            >
              {loading ? (
                <span className="button-spinner"></span>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd"/>
                  </svg>
                  Explain
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="jargon-alert jargon-alert-error">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
              </svg>
              {error}
            </div>
          )}
        </div>

        {/* Result Card */}
        {result && (
          <div className="jargon-result-card">
            <div className="result-header">
              <div className="result-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <h2>{result.term}</h2>
                <span className="result-pronunciation">{result.pronunciation}</span>
              </div>
            </div>

            <div className="result-section">
              <div className="result-label">
                <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                </svg>
                Definition
              </div>
              <p className="result-text">{result.definition}</p>
            </div>

            {result.example && result.example !== "No example available." && (
              <div className="result-section">
                <div className="result-label">
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z" clipRule="evenodd"/>
                  </svg>
                  Example
                </div>
                <p className="result-example">{result.example}</p>
              </div>
            )}
          </div>
        )}

        {/* Content Grid */}
        <div className="jargon-content-grid">
          {/* Popular Terms */}
          <div className="jargon-section">
            <h3 className="section-heading">Popular Medical Terms</h3>
            <div className="popular-terms-grid">
              {popularTerms.map((item, index) => (
                <div
                  key={index}
                  className="popular-term-card"
                  onClick={() => explainTerm(item.term)}
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <div className="term-icon">{item.icon}</div>
                  <div className="term-info">
                    <span className="term-name">{item.term}</span>
                    <span className="term-category">{item.category}</span>
                  </div>
                  <svg className="term-arrow" width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                  </svg>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Searches */}
          {recentSearches.length > 0 && (
            <div className="jargon-section">
              <h3 className="section-heading">Recent Searches</h3>
              <div className="recent-searches-list">
                {recentSearches.map((term, index) => (
                  <div
                    key={index}
                    className="recent-search-chip"
                    onClick={() => explainTerm(term)}
                  >
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd"/>
                    </svg>
                    {term}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default JargonBuster;