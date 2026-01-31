import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import '../App.css';

function HealthRiskAssessment({ darkMode, setDarkMode }) {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const [loading, setLoading] = useState(true);
  const [riskData, setRiskData] = useState(null);
  const [error, setError] = useState('');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const calculateRisks = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 
       (process.env.NODE_ENV === 'production'
         ? 'https://my-repo-production-276b.up.railway.app'
         : 'http://localhost:5000');

      const response = await axios.get(
        `${API_BASE_URL}/api/report/calculate-risks/${reportId}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setRiskData(response.data.risks);
    } catch (err) {
      console.error('Risk calculation error:', err);
      setError(err.response?.data?.error || 'Failed to calculate health risks');
    } finally {
      setLoading(false);
    }
  }, [reportId]);

  useEffect(() => {
    calculateRisks();
  }, [calculateRisks]);

  const getRiskColor = (level) => {
    switch (level) {
      case 'LOW':
      case 'NORMAL':
        return '#10B981';
      case 'MEDIUM':
      case 'MODERATE_RISK':
      case 'PREDIABETIC':
        return '#F59E0B';
      case 'HIGH':
      case 'HIGH_RISK':
      case 'DIABETIC':
        return '#EF4444';
      default:
        return '#6B7280';
    }
  };

  const getRiskIcon = (level) => {
    const color = getRiskColor(level);
    switch (level) {
      case 'LOW':
      case 'NORMAL':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill={color}>
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
          </svg>
        );
      case 'MEDIUM':
      case 'MODERATE_RISK':
      case 'PREDIABETIC':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill={color}>
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
          </svg>
        );
      case 'HIGH':
      case 'HIGH_RISK':
      case 'DIABETIC':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill={color}>
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
          </svg>
        );
      default:
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill={color}>
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd"/>
          </svg>
        );
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return '#10B981';
    if (score >= 75) return '#22C55E';
    if (score >= 60) return '#F59E0B';
    if (score >= 40) return '#F97316';
    return '#EF4444';
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'cardiovascular':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd"/>
          </svg>
        );
      case 'diabetes':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" clipRule="evenodd"/>
          </svg>
        );
      case 'kidney':
        return (
          <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/>
          </svg>
        );
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="dashboard-wrapper">
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

        <div className="modern-loading-state">
          <div className="loading-spinner"></div>
          <h3>Calculating Health Risks</h3>
          <p>Analyzing your medical data to assess potential health risks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-wrapper">
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

        <div className="modern-empty-state">
          <div className="empty-icon-wrapper">
            <svg width="64" height="64" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
            </svg>
          </div>
          <h3>Unable to Calculate Risks</h3>
          <p>{error}</p>
          <button onClick={() => navigate('/dashboard')} className="btn-get-started">
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

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

      <div className="risk-assessment-container">
        {/* Page Header */}
        <div className="risk-header">
          <div className="risk-header-icon">
            <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
            </svg>
          </div>
          <div>
            <h1>Health Risk Assessment</h1>
            <p>Comprehensive analysis of your health indicators</p>
          </div>
        </div>

        {/* Overall Health Score */}
        <div className="health-score-card">
          <h2>Overall Health Score</h2>
          <div className="score-circle">
            <svg width="200" height="200" viewBox="0 0 200 200">
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="var(--border)"
                strokeWidth="12"
              />
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke={getScoreColor(riskData.overall_score)}
                strokeWidth="12"
                strokeDasharray={`${(riskData.overall_score / 100) * 565.48} 565.48`}
                strokeLinecap="round"
                transform="rotate(-90 100 100)"
                style={{ transition: 'stroke-dasharray 1s ease' }}
              />
              <text x="100" y="95" textAnchor="middle" fontSize="48" fontWeight="700" fill="var(--text)">
                {riskData.overall_score}
              </text>
              <text x="100" y="120" textAnchor="middle" fontSize="16" fill="var(--text-light)">
                out of 100
              </text>
            </svg>
          </div>
          <h3 className="score-status">{riskData.overall_status}</h3>
          <p className="score-message">{riskData.overall_message}</p>
        </div>

        {/* Risk Categories */}
        <div className="risk-categories">
          {/* Cardiovascular Risk */}
          {riskData.cardiovascular && (
            <div className="risk-category-card" style={{ borderColor: getRiskColor(riskData.cardiovascular.level) }}>
              <div className="category-header">
                <div className="category-icon cardiovascular-icon">
                  {getCategoryIcon('cardiovascular')}
                </div>
                <div className="category-info">
                  <h3>Cardiovascular Risk</h3>
                  <div className="risk-badge" style={{ background: getRiskColor(riskData.cardiovascular.level) }}>
                    {getRiskIcon(riskData.cardiovascular.level)}
                    <span>{riskData.cardiovascular.level}</span>
                  </div>
                </div>
              </div>

              <div className="category-section">
                <div className="section-title">
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                  </svg>
                  Risk Factors
                </div>
                <ul className="factor-list">
                  {riskData.cardiovascular.factors.map((factor, idx) => (
                    <li key={idx}>{factor}</li>
                  ))}
                </ul>
              </div>

              {riskData.cardiovascular.recommendations.length > 0 && (
                <div className="category-section">
                  <div className="section-title">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/>
                    </svg>
                    Recommendations
                  </div>
                  <ul className="recommendation-list">
                    {riskData.cardiovascular.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Diabetes Risk */}
          {riskData.diabetes && (
            <div className="risk-category-card" style={{ borderColor: getRiskColor(riskData.diabetes.level) }}>
              <div className="category-header">
                <div className="category-icon diabetes-icon">
                  {getCategoryIcon('diabetes')}
                </div>
                <div className="category-info">
                  <h3>Diabetes Risk</h3>
                  <div className="risk-badge" style={{ background: getRiskColor(riskData.diabetes.level) }}>
                    {getRiskIcon(riskData.diabetes.level)}
                    <span>{riskData.diabetes.level}</span>
                  </div>
                </div>
              </div>

              <div className="category-section">
                <div className="section-title">
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                  </svg>
                  Risk Factors
                </div>
                <ul className="factor-list">
                  {riskData.diabetes.factors.map((factor, idx) => (
                    <li key={idx}>{factor}</li>
                  ))}
                </ul>
              </div>

              {riskData.diabetes.recommendations.length > 0 && (
                <div className="category-section">
                  <div className="section-title">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/>
                    </svg>
                    Recommendations
                  </div>
                  <ul className="recommendation-list">
                    {riskData.diabetes.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Kidney Health */}
          {riskData.kidney && (
            <div className="risk-category-card" style={{ borderColor: getRiskColor(riskData.kidney.level) }}>
              <div className="category-header">
                <div className="category-icon kidney-icon">
                  {getCategoryIcon('kidney')}
                </div>
                <div className="category-info">
                  <h3>Kidney Health</h3>
                  <div className="risk-badge" style={{ background: getRiskColor(riskData.kidney.level) }}>
                    {getRiskIcon(riskData.kidney.level)}
                    <span>{riskData.kidney.level.replace('_', ' ')}</span>
                  </div>
                </div>
              </div>

              <div className="category-section">
                <div className="section-title">
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                  </svg>
                  Risk Factors
                </div>
                <ul className="factor-list">
                  {riskData.kidney.factors.map((factor, idx) => (
                    <li key={idx}>{factor}</li>
                  ))}
                </ul>
              </div>

              {riskData.kidney.recommendations.length > 0 && (
                <div className="category-section">
                  <div className="section-title">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/>
                    </svg>
                    Recommendations
                  </div>
                  <ul className="recommendation-list">
                    {riskData.kidney.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Overall Recommendations */}
        {riskData.recommendations && riskData.recommendations.length > 0 && (
          <div className="overall-recommendations">
            <h3>Overall Health Recommendations</h3>
            <ul>
              {riskData.recommendations.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Buttons */}
        <div className="risk-actions">
          <button onClick={() => navigate(`/report/${reportId}`)} className="btn-secondary-action">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd"/>
            </svg>
            Back to Report
          </button>
          <button onClick={() => navigate('/dashboard')} className="btn-primary-action">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
            </svg>
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default HealthRiskAssessment;