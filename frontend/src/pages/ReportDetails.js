import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import '../App.css';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

function ReportDetails() {
  const { reportId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const printRef = useRef();

  useEffect(() => {
    console.log('Loading report with ID:', reportId);
    
    if (!reportId || reportId === 'undefined') {
      console.error('Invalid report ID!');
      setLoading(false);
      return;
    }
    
    reportAPI.getDetails(reportId)
      .then(res => {
        console.log('Report loaded successfully:', res.data);
        setReport(res.data);
      })
      .catch((err) => {
        console.error('Failed to load report:', err);
        alert('Failed to load report');
      })
      .finally(() => setLoading(false));
  }, [reportId]);

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

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner"></div>
        <p>Loading report...</p>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="error-message">
        <h2>Report not found</h2>
        <p>The report you're looking for doesn't exist or has been deleted.</p>
        <button onClick={() => navigate('/dashboard')} className="btn-primary">
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="report-details-container">
      <div className="report-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <button onClick={() => navigate('/dashboard')} className="btn-back">
          ← Back to Dashboard
        </button>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={isSpeaking ? stopSpeaking : speakSummary}
            className="btn-primary"
            style={{ padding: '10px 20px', fontSize: '14px' }}
          >
            {isSpeaking ? 'Stop Reading' : 'Read Aloud'}
          </button>
          <button onClick={exportToPDF} className="btn-primary" style={{ padding: '10px 20px', fontSize: '14px' }}>
            Export to PDF
          </button>
        </div>
      </div>

      <div ref={printRef} className="report-print-area">
        <div className="report-header">
          <h1 style={{ fontSize: '28px', margin: '0 0 8px', fontWeight: 600 }}>
            {report.filename}
          </h1>
          <p className="report-date">
            Uploaded: {report.uploaded_at}
          </p>
        </div>

        {/* FIXED: Verification Badge with Readable Text */}
        {report.verification_enabled && report.verification && (
          <div style={{
            marginBottom: '24px',
            padding: '20px',
            borderRadius: '12px',
            border: `3px solid ${
              report.verification.trust_score >= 70 ? '#10B981' : 
              report.verification.trust_score >= 50 ? '#F59E0B' : '#EF4444'
            }`,
            background: `${
              report.verification.trust_score >= 70 ? '#ECFDF5' : 
              report.verification.trust_score >= 50 ? '#FFFBEB' : '#FEF2F2'
            }`,
            color: `${
              report.verification.trust_score >= 70 ? '#065F46' : 
              report.verification.trust_score >= 50 ? '#78350F' : '#991B1B'
            }`
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
              <span style={{ fontSize: '32px', marginRight: '12px' }}>
                {report.verification.trust_score >= 70 ? '✅' : 
                 report.verification.trust_score >= 50 ? '⚠️' : '🚨'}
              </span>
              <div>
                <h3 style={{ 
                  margin: 0, 
                  fontSize: '20px', 
                  fontWeight: 700,
                  color: report.verification.trust_score >= 70 ? '#047857' : 
                         report.verification.trust_score >= 50 ? '#B45309' : '#DC2626'
                }}>
                  {report.verification.risk_level}
                </h3>
                <p style={{ 
                  margin: '4px 0 0', 
                  fontSize: '16px', 
                  fontWeight: 600,
                  color: report.verification.trust_score >= 70 ? '#059669' : 
                         report.verification.trust_score >= 50 ? '#D97706' : '#EF4444'
                }}>
                  Trust Score: {report.verification.trust_score}/100
                </p>
              </div>
            </div>

            {report.verification.findings && report.verification.findings.length > 0 && (
              <div style={{ marginTop: '16px' }}>
                <strong style={{ 
                  fontSize: '15px', 
                  display: 'block', 
                  marginBottom: '8px',
                  color: report.verification.trust_score >= 70 ? '#047857' : 
                         report.verification.trust_score >= 50 ? '#92400E' : '#991B1B'
                }}>
                  📋 Findings:
                </strong>
                <ul style={{ 
                  margin: '0', 
                  paddingLeft: '24px', 
                  fontSize: '14px',
                  lineHeight: '1.8',
                  color: report.verification.trust_score >= 70 ? '#065F46' : 
                         report.verification.trust_score >= 50 ? '#78350F' : '#991B1B'
                }}>
                  {report.verification.findings.map((finding, idx) => (
                    <li key={idx} style={{ marginBottom: '6px' }}>{finding}</li>
                  ))}
                </ul>
              </div>
            )}

            {report.verification.recommendations && report.verification.recommendations.length > 0 && (
              <div style={{ marginTop: '16px' }}>
                <strong style={{ 
                  fontSize: '15px', 
                  display: 'block', 
                  marginBottom: '8px',
                  color: report.verification.trust_score >= 70 ? '#047857' : 
                         report.verification.trust_score >= 50 ? '#92400E' : '#991B1B'
                }}>
                  💡 Recommendations:
                </strong>
                <ul style={{ 
                  margin: '0', 
                  paddingLeft: '24px', 
                  fontSize: '14px',
                  lineHeight: '1.8',
                  color: report.verification.trust_score >= 70 ? '#065F46' : 
                         report.verification.trust_score >= 50 ? '#78350F' : '#991B1B'
                }}>
                  {report.verification.recommendations.map((rec, idx) => (
                    <li key={idx} style={{ marginBottom: '6px' }}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <div className="summary-section" style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', margin: '0 0 16px', fontWeight: 600 }}>
            Plain Language Summary
          </h2>
          <div className="summary-box" style={{ whiteSpace: 'pre-wrap' }}>
            {report.plain_language_summary}
          </div>
        </div>

        {/* Health Risk Assessment Button - Light Blue Color */}
        <div style={{ marginTop: '24px', textAlign: 'center' }}>
          <button
            onClick={() => navigate(`/risk-assessment/${reportId}`)}
            className="btn-primary"
            style={{
              padding: '16px 32px',
              fontSize: 16,
              background: '#60A5FA',  // Light blue color
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '500',
              transition: 'background 0.2s',
              color: 'white'
            }}
            onMouseEnter={(e) => e.target.style.background = '#3B82F6'}
            onMouseLeave={(e) => e.target.style.background = '#60A5FA'}
          >
            ⚠️ Calculate Health Risks
          </button>
        </div>

        <div className="original-text-section">
          <h2 style={{ fontSize: '20px', margin: '0 0 16px', fontWeight: 600 }}>
            Original Extracted Text
          </h2>
          <details style={{ marginTop: '8px' }}>
            <summary style={{ cursor: 'pointer', color: 'var(--primary)', fontWeight: 500 }}>
              ▼ Click to expand
            </summary>
            <div className="original-text-box" style={{ whiteSpace: 'pre-wrap', marginTop: '12px' }}>
              {report.extracted_text}
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}

export default ReportDetails;