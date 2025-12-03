import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import '../App.css';

function History() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    reportAPI.getHistory()
      .then(res => setReports(res.data.reports))
      .catch(() => alert('Failed to load history'))
      .finally(() => setLoading(false));
  }, []);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const today = new Date();
    const diff = Math.floor((today - date) / (1000 * 60 * 60 * 24));

    if (diff === 0) return { label: 'Today', time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    if (diff === 1) return { label: 'Yesterday', time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    if (diff <= 7) return { label: 'This Week', time: date.toLocaleDateString() };
    return { label: 'Older', time: date.toLocaleDateString() };
  };

  const grouped = reports.reduce((acc, r) => {
    const { label } = formatDate(r.uploaded_at);
    if (!acc[label]) acc[label] = [];
    acc[label].push(r);
    return acc;
  }, {});

  const order = ['Today', 'Yesterday', 'This Week', 'Older'];

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Medical Report Summarizer</h1>
        <div className="user-info">
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">← Back</button>
          <span>Welcome, {localStorage.getItem('username')}!</span>
          <button onClick={() => { localStorage.clear(); navigate('/login'); }} className="btn-logout">Logout</button>
        </div>
      </div>

      <div className="history-page">
        <h2>Your Reports History</h2>
        <p className="history-subtitle">View all your uploaded medical reports</p>

        {loading ? (
          <div className="loading-state"><div className="spinner"></div><p>Loading...</p></div>
        ) : reports.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">Empty</span>
            <p>No reports yet. Upload your first one!</p>
            <button onClick={() => navigate('/dashboard')} className="btn-primary">Upload Report</button>
          </div>
        ) : (
          <div className="timeline-container">
            {order.map(label => grouped[label] && (
              <div key={label} className="timeline-group">
                <h3 className="timeline-header">{label}</h3>
                {grouped[label].map(r => (
                  <div key={r.id} className="timeline-item">
                    <div className="timeline-marker"></div>
                    <div className="timeline-content">
                      <div className="timeline-item-header">
                        <h4>{r.filename}</h4>
                        <span className="timeline-time">{formatDate(r.uploaded_at).time}</span>
                      </div>
                      <p className="timeline-summary">
                        {r.plain_summary?.substring(0, 120)}...
                      </p>
                      <button onClick={() => navigate(`/report/${r.id}`)} className="btn-view-timeline">
                        View Summary →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default History;
