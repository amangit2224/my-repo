// src/pages/HealthRiskAssessment.js
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import '../App.css';

function HealthRiskAssessment() {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [riskData, setRiskData] = useState(null);
  const [error, setError] = useState('');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const calculateRisks = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const API_BASE_URL = process.env.NODE_ENV === 'production'
        ? 'https://medical-backend-wbqv.onrender.com'
        : 'http://localhost:5000';

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
        return '#10B981'; // Green
      case 'MEDIUM':
      case 'MODERATE_RISK':
      case 'PREDIABETIC':
        return '#F59E0B'; // Orange
      case 'HIGH':
      case 'HIGH_RISK':
      case 'DIABETIC':
        return '#EF4444'; // Red
      default:
        return '#6B7280'; // Gray
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'LOW':
      case 'NORMAL':
        return '✅';
      case 'MEDIUM':
      case 'MODERATE_RISK':
      case 'PREDIABETIC':
        return '⚠️';
      case 'HIGH':
      case 'HIGH_RISK':
      case 'DIABETIC':
        return '🔴';
      default:
        return '❓';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return '#10B981';
    if (score >= 75) return '#22C55E';
    if (score >= 60) return '#F59E0B';
    if (score >= 40) return '#F97316';
    return '#EF4444';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>⚠️ Health Risk Assessment</h1>
          <div className="user-info">
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back
            </button>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
        <div className="loading-state">
          <div className="spinner" />
          <p>Calculating your health risks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>⚠️ Health Risk Assessment</h1>
          <div className="user-info">
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back
            </button>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
        <div className="upload-section" style={{ padding: 32 }}>
          <div className="empty-state">
            <span className="empty-icon">⚠️</span>
            <p>{error}</p>
            <button onClick={() => navigate('/dashboard')} className="btn-primary">
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <h1>⚠️ Health Risk Assessment</h1>
        <div className="user-info">
          <button onClick={() => navigate(`/report/${reportId}`)} className="btn-secondary">
            Back to Report
          </button>
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            Dashboard
          </button>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="upload-section" style={{ padding: 32, maxWidth: 1000, margin: '0 auto' }}>
        
        {/* Overall Health Score */}
        <div style={{
          background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
          borderRadius: 16,
          padding: 32,
          marginBottom: 32,
          color: 'white',
          textAlign: 'center'
        }}>
          <h2 style={{ fontSize: 28, marginBottom: 16 }}>Overall Health Score</h2>
          <div style={{ fontSize: 64, fontWeight: 'bold', marginBottom: 8 }}>
            {riskData.overall_score}/100
          </div>
          <div style={{ fontSize: 20, marginBottom: 20, opacity: 0.9 }}>
            {riskData.overall_status}
          </div>
          
          {/* Progress Bar */}
          <div style={{
            width: '100%',
            height: 12,
            background: 'rgba(255,255,255,0.3)',
            borderRadius: 6,
            overflow: 'hidden',
            marginBottom: 16
          }}>
            <div style={{
              width: `${riskData.overall_score}%`,
              height: '100%',
              background: getScoreColor(riskData.overall_score),
              transition: 'width 1s ease'
            }} />
          </div>
          
          <p style={{ fontSize: 16, opacity: 0.95, margin: 0 }}>
            {riskData.overall_message}
          </p>
        </div>

        {/* Risk Categories */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr',
          gap: 24,
          marginBottom: 32
        }}>
          
          {/* Cardiovascular Risk */}
          {riskData.cardiovascular && (
            <div style={{
              background: 'white',
              borderRadius: 12,
              padding: 24,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: `3px solid ${getRiskColor(riskData.cardiovascular.level)}`
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 16
              }}>
                <h3 style={{ fontSize: 20, margin: 0 }}>
                  ❤️ Cardiovascular Risk
                </h3>
                <div style={{
                  fontSize: 24,
                  fontWeight: 'bold',
                  color: getRiskColor(riskData.cardiovascular.level)
                }}>
                  {getRiskIcon(riskData.cardiovascular.level)} {riskData.cardiovascular.level}
                </div>
              </div>
              
              <div style={{ marginBottom: 16 }}>
                <strong>Factors:</strong>
                <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                  {riskData.cardiovascular.factors.map((factor, idx) => (
                    <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
              
              {riskData.cardiovascular.recommendations.length > 0 && (
                <div>
                  <strong>Recommendations:</strong>
                  <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                    {riskData.cardiovascular.recommendations.map((rec, idx) => (
                      <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Diabetes Risk */}
          {riskData.diabetes && (
            <div style={{
              background: 'white',
              borderRadius: 12,
              padding: 24,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: `3px solid ${getRiskColor(riskData.diabetes.level)}`
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 16
              }}>
                <h3 style={{ fontSize: 20, margin: 0 }}>
                  🩸 Diabetes Risk
                </h3>
                <div style={{
                  fontSize: 24,
                  fontWeight: 'bold',
                  color: getRiskColor(riskData.diabetes.level)
                }}>
                  {getRiskIcon(riskData.diabetes.level)} {riskData.diabetes.level}
                </div>
              </div>
              
              <div style={{ marginBottom: 16 }}>
                <strong>Factors:</strong>
                <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                  {riskData.diabetes.factors.map((factor, idx) => (
                    <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
              
              {riskData.diabetes.recommendations.length > 0 && (
                <div>
                  <strong>Recommendations:</strong>
                  <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                    {riskData.diabetes.recommendations.map((rec, idx) => (
                      <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Kidney Health */}
          {riskData.kidney && (
            <div style={{
              background: 'white',
              borderRadius: 12,
              padding: 24,
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
              border: `3px solid ${getRiskColor(riskData.kidney.level)}`
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: 16
              }}>
                <h3 style={{ fontSize: 20, margin: 0 }}>
                  🫘 Kidney Health
                </h3>
                <div style={{
                  fontSize: 24,
                  fontWeight: 'bold',
                  color: getRiskColor(riskData.kidney.level)
                }}>
                  {getRiskIcon(riskData.kidney.level)} {riskData.kidney.level.replace('_', ' ')}
                </div>
              </div>
              
              <div style={{ marginBottom: 16 }}>
                <strong>Factors:</strong>
                <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                  {riskData.kidney.factors.map((factor, idx) => (
                    <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
              
              {riskData.kidney.recommendations.length > 0 && (
                <div>
                  <strong>Recommendations:</strong>
                  <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                    {riskData.kidney.recommendations.map((rec, idx) => (
                      <li key={idx} style={{ marginBottom: 4, color: 'var(--text-secondary)' }}>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Overall Recommendations */}
        {riskData.recommendations && riskData.recommendations.length > 0 && (
          <div style={{
            background: 'var(--primary-light)',
            borderRadius: 12,
            padding: 24,
            border: '2px solid var(--primary)'
          }}>
            <h3 style={{ fontSize: 20, marginBottom: 16 }}>📋 Overall Recommendations</h3>
            <ul style={{ paddingLeft: 20, margin: 0 }}>
              {riskData.recommendations.map((rec, idx) => (
                <li key={idx} style={{ marginBottom: 8, fontSize: 15 }}>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Action Buttons */}
        <div style={{
          display: 'flex',
          gap: 16,
          justifyContent: 'center',
          marginTop: 32
        }}>
          <button
            onClick={() => navigate(`/report/${reportId}`)}
            className="btn-secondary"
          >
            Back to Report
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn-primary"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default HealthRiskAssessment;