import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import '../App.css';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

function ReportDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const printRef = useRef();

  useEffect(() => {
    reportAPI.getDetails(id)
      .then(res => setReport(res.data))
      .catch(() => alert('Failed to load report'))
      .finally(() => setLoading(false));
  }, [id]);

  const speakSummary = () => {
    if (!report?.plain_language_summary || isSpeaking) return;
    const text = report.plain_language_summary.replace(/[*→]/g, '');
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

  // render element to a high-res canvas
  const canvas = await html2canvas(element, {
    scale: 2,
    useCORS: true,
    backgroundColor: getComputedStyle(document.body).getPropertyValue('--bg').trim() || '#FFFFFF',
  });

  // Create a PDF in "pt" (points) which makes pixel math easier
  const pdf = new jsPDF('p', 'pt', 'a4');
  const pageWidthPt = pdf.internal.pageSize.getWidth();   // points
  const pageHeightPt = pdf.internal.pageSize.getHeight(); // points

  // Map canvas pixels -> PDF pts
  const pxPerPt = canvas.width / pageWidthPt;           // canvas px per PDF point
  const pageHeightPx = Math.floor(pageHeightPt * pxPerPt); // how many canvas px fit into one PDF page

  let y = 0;
  let pageCount = 0;

  while (y < canvas.height) {
    // slice a portion of the canvas
    const sliceHeightPx = Math.min(pageHeightPx, canvas.height - y);
    const tmpCanvas = document.createElement('canvas');
    tmpCanvas.width = canvas.width;
    tmpCanvas.height = sliceHeightPx;
    const tmpCtx = tmpCanvas.getContext('2d');

    // draw the slice from the big canvas onto temporary canvas
    tmpCtx.drawImage(canvas, 0, y, canvas.width, sliceHeightPx, 0, 0, canvas.width, sliceHeightPx);

    const imgData = tmpCanvas.toDataURL('image/png');

    // Convert slice height (px) to PDF points for the image height on page
    const imgHeightPt = sliceHeightPx / pxPerPt;

    if (pageCount > 0) pdf.addPage();
    // optional: add a small top margin (10pt)
    pdf.addImage(imgData, 'PNG', 10, 10, pageWidthPt - 20, imgHeightPt - 0);
    y += sliceHeightPx;
    pageCount += 1;
  }

  pdf.save(`${report.filename.replace(/\.[^/.]+$/, '')}_summary.pdf`);
};



  if (loading) return <div className="loading-state"><div className="spinner"></div><p>Loading report...</p></div>;
  if (!report) return <div className="error-message">Report not found</div>;

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
          <h1 style={{ fontSize: '28px', margin: '0 0 8px', fontWeight: 600 }}>{report.filename}</h1>
          <p className="report-date">
            Uploaded: {new Date(report.uploaded_at).toLocaleString()}
          </p>
        </div>

        <div className="summary-section" style={{ marginBottom: '32px' }}>
          <h2 style={{ fontSize: '20px', margin: '0 0 16px', fontWeight: 600 }}>
            Plain Language Summary
          </h2>
          <div className="summary-box">
            {report.plain_language_summary}
          </div>
        </div>

        <div className="original-text-section">
          <h2 style={{ fontSize: '20px', margin: '0 0 16px', fontWeight: 600 }}>
            Original Extracted Text
          </h2>
          <details style={{ marginTop: '8px' }}>
            <summary style={{ cursor: 'pointer', color: 'var(--primary)', fontWeight: 500 }}>
              Click to expand
            </summary>
            <div className="original-text-box">
              {report.extracted_text}
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}

export default ReportDetails;
