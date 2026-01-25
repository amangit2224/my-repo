import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import '../App.css';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import DietModal from '../components/DietModal';
import ChatSection from '../components/ChatSection';

function ReportDetails({ darkMode, setDarkMode }) {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [dietModalOpen, setDietModalOpen] = useState(false);
  const [dietPlan, setDietPlan] = useState(null);
  const [loadingDiet, setLoadingDiet] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const printRef = useRef();

  useEffect(() => {
    if (!reportId || reportId === 'undefined') {
      setLoading(false);
      return;
    }
    
    reportAPI.getDetails(reportId)
      .then(res => {
        setReport(res.data);
      })
      .catch((err) => {
        console.error('Failed to load report:', err);
        alert('Failed to load report');
      })
      .finally(() => setLoading(false));
  }, [reportId]);

  const fetchDietRecommendations = async () => {
    setLoadingDiet(true);
    setDietModalOpen(true);
    
    try {
      const response = await reportAPI.getDietRecommendations(reportId);
      setDietPlan(response.data.diet_plan);
    } catch (error) {
      console.error('Error fetching diet recommendations:', error);
      alert(error.response?.data?.error || 'Failed to load diet recommendations');
      setDietModalOpen(false);
    } finally {
      setLoadingDiet(false);
    }
  };

  const speakSummary = () => {
    if (!report?.plain_language_summary || isSpeaking) return;
    const text = report.plain_language_summary.replace(/[*→#]/g, '');
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const exportToPDF = async () => {
    const element = printRef.current;
    if (!element) return;

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      backgroundColor: getComputedStyle(document.body).getPropertyValue('--bg').trim() || '#FFFFFF',
    });

    const pdf = new jsPDF('p', 'pt', 'a4');
    const pageWidthPt = pdf.internal.pageSize.getWidth();
    const pageHeightPt = pdf.internal.pageSize.getHeight();
    const pxPerPt = canvas.width / pageWidthPt;
    const pageHeightPx = Math.floor(pageHeightPt * pxPerPt);

    let y = 0;
    let pageCount = 0;

    while (y < canvas.height) {
      const sliceHeightPx = Math.min(pageHeightPx, canvas.height - y);
      const tmpCanvas = document.createElement('canvas');
      tmpCanvas.width = canvas.width;
      tmpCanvas.height = sliceHeightPx;
      const tmpCtx = tmpCanvas.getContext('2d');
      tmpCtx.drawImage(canvas, 0, y, canvas.width, sliceHeightPx, 0, 0, canvas.width, sliceHeightPx);

      const imgData = tmpCanvas.toDataURL('image/png');
      const imgHeightPt = sliceHeightPx / pxPerPt;

      if (pageCount > 0) pdf.addPage();
      pdf.addImage(imgData, 'PNG', 10, 10, pageWidthPt - 20, imgHeightPt);
      y += sliceHeightPx;
      pageCount += 1;
    }

    pdf.save(`${report.filename.replace(/\.[^/.]+$/, '')}_summary.pdf`);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  if (loading) {
    return (
      <div className="modern-loading-state">
        <div className="loading-spinner"></div>
        <h3>Loading report...</h3>
        <p>Please wait while we fetch your medical data</p>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="modern-error-state">
        <div className="error-icon-wrapper">
          <svg width="64" height="64" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
          </svg>
        </div>
        <h2>Report Not Found</h2>
        <p>The report you're looking for doesn't exist or has been deleted</p>
        <button onClick={() => navigate('/dashboard')} className="btn-get-started">
          Back to Dashboard
        </button>
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

      <div className="report-details-container">
        {/* Header Actions */}
        <div className="report-actions-header">
          <button onClick={() => navigate('/dashboard')} className="btn-back-action">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd"/>
            </svg>
            Back to Dashboard
          </button>
          <div className="action-buttons">
            <button onClick={isSpeaking ? stopSpeaking : speakSummary} className="btn-action">
              {isSpeaking ? (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z" clipRule="evenodd"/>
                </svg>
              )}
              {isSpeaking ? 'Stop' : 'Read Aloud'}
            </button>
            <button onClick={exportToPDF} className="btn-action btn-primary-action">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clipRule="evenodd"/>
              </svg>
              Export to PDF
            </button>
          </div>
        </div>

        <div ref={printRef} className="report-content">
          {/* Report Header */}
          <div className="report-info-card">
            <div className="report-file-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div className="report-info-content">
              <h1>{report.filename}</h1>
              <div className="report-meta">
                <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd"/>
                </svg>
                Uploaded: {report.uploaded_at}
              </div>
            </div>
          </div>

          {/* Verification Badge */}
          {report.verification_enabled && report.verification && (
            <div className={`verification-card ${
              report.verification.trust_score >= 70 ? 'verified' : 
              report.verification.trust_score >= 50 ? 'warning' : 'danger'
            }`}>
              <div className="verification-header">
                <div className="verification-icon">
                  {report.verification.trust_score >= 70 ? (
                    <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                  ) : report.verification.trust_score >= 50 ? (
                    <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                    </svg>
                  ) : (
                    <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                    </svg>
                  )}
                </div>
                <div className="verification-info">
                  <h3>{report.verification.risk_level}</h3>
                  <div className="trust-score-wrapper">
                    <span className="trust-label">Trust Score</span>
                    <div className="trust-score-bar">
                      <div 
                        className="trust-score-fill"
                        style={{ width: `${report.verification.trust_score}%` }}
                      ></div>
                    </div>
                    <span className="trust-value">{report.verification.trust_score}/100</span>
                  </div>
                </div>
              </div>

              {report.verification.findings && report.verification.findings.length > 0 && (
                <div className="verification-section">
                  <div className="section-label">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                    </svg>
                    Findings
                  </div>
                  <ul className="verification-list">
                    {report.verification.findings.map((finding, idx) => (
                      <li key={idx}>{finding}</li>
                    ))}
                  </ul>
                </div>
              )}

              {report.verification.recommendations && report.verification.recommendations.length > 0 && (
                <div className="verification-section">
                  <div className="section-label">
                    <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/>
                    </svg>
                    Recommendations
                  </div>
                  <ul className="verification-list">
                    {report.verification.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Summary Section with Scroll */}
          <div className="summary-section-modern">
            <h2>Plain Language Summary</h2>
            <div className="summary-scrollable">
              {report.plain_language_summary}
            </div>
          </div>

          {/* Action Cards Grid */}
          <div className="action-cards-grid">
            <div className="action-card-feature" onClick={() => navigate(`/risk-assessment/${reportId}`)}>
              <div className="action-card-icon risk-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>Health Risk Assessment</h3>
                <p>Calculate your health risks based on this report</p>
              </div>
              <div className="action-card-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>

            <div className="action-card-feature" onClick={fetchDietRecommendations}>
              <div className="action-card-icon diet-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>Personalized Diet Plan</h3>
                <p>Get nutrition recommendations tailored to your results</p>
              </div>
              <div className="action-card-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>

            <div className="action-card-feature" onClick={() => setChatOpen(!chatOpen)}>
              <div className="action-card-icon chat-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>{chatOpen ? 'Close Chat' : 'Chat with Report'}</h3>
                <p>Ask questions about your medical report</p>
              </div>
              <div className="action-card-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>
          </div>

          {/* Chat Section */}
          <ChatSection 
            reportId={reportId}
            isOpen={chatOpen}
            onClose={() => setChatOpen(false)}
          />

          {/* Original Text - Collapsible */}
          <div className="original-text-section-modern">
            <details>
              <summary>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V8z" clipRule="evenodd"/>
                </svg>
                Original Extracted Text
              </summary>
              <div className="original-text-content">
                {report.extracted_text}
              </div>
            </details>
          </div>
        </div>
      </div>

      {/* Diet Modal */}
      <DietModal 
        isOpen={dietModalOpen}
        onClose={() => setDietModalOpen(false)}
        dietPlan={dietPlan}
        loading={loadingDiet}
      />
    </div>
  );
}

export default ReportDetails;