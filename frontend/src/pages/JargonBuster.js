import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jargonAPI } from '../utils/api';
import '../App.css';

function JargonBuster() {
  const [search, setSearch] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const explainTerm = async () => {
    if (!search.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await jargonAPI.explain(search.trim());
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Could not explain term. Try another.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Jargon Buster</h1>
        <div className="user-info">
          <button onClick={() => navigate(-1)} className="btn-secondary">Back</button>
          <button onClick={() => { localStorage.clear(); navigate('/login'); }} className="btn-logout">Logout</button>
        </div>
      </div>

      <div className="upload-section" style={{ padding: '32px' }}>
        <h2>Explain Any Medical Term</h2>
        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
          <input
            type="text"
            placeholder="ask here"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && explainTerm()}
            style={{ flex: 1, padding: '14px 16px', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '16px', background: 'var(--bg)' }}
          />
          <button onClick={explainTerm} disabled={loading} className="btn-primary" style={{ padding: '0 24px' }}>
            {loading ? '...' : 'Explain'}
          </button>
        </div>

        {error && <p style={{ color: 'var(--danger)', textAlign: 'center' }}>{error}</p>}

        {result && (
          <div className="action-card result-card" style={{ padding: '24px', borderRadius: '12px' }}>
            <h3 style={{ margin: '0 0 16px', fontSize: '22px', color: 'var(--text)', fontWeight: '600' }}>
              {result.term}
            </h3>

            <div style={{ marginBottom: '14px' }}>
              <strong style={{ color: 'var(--text)' }}>Pronunciation:</strong>
              <span style={{ color: 'var(--danger)', marginLeft: '8px', fontWeight: '500' }}>
                {result.pronunciation}
              </span>
            </div>

            <div style={{ marginBottom: '14px' }}>
              <strong style={{ color: 'var(--text)' }}>Definition:</strong>
              <p style={{ margin: '8px 0 0', lineHeight: '1.6', color: 'var(--text)' }}>
                {result.definition}
              </p>
            </div>

            {result.example && result.example !== "No example available." && (
              <div>
                <strong style={{ color: 'var(--text)' }}>Example:</strong>
                <p style={{ margin: '8px 0 0', lineHeight: '1.6', fontStyle: 'italic', color: 'var(--primary)' }}>
                  {result.example}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default JargonBuster;
