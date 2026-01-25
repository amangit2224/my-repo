import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js';
import '../App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function HealthTrends({ darkMode, setDarkMode }) {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const [report1, setReport1] = useState(null);
  const [report2, setReport2] = useState(null);
  const [comparing, setComparing] = useState(false);
  const [comparisonData, setComparisonData] = useState(null);
  const [error, setError] = useState('');
  
  const fileInput1Ref = useRef(null);
  const fileInput2Ref = useRef(null);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleFileSelect = (fileNum, file) => {
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
      setError('Please upload PDF files only');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }
    
    setError('');
    
    if (fileNum === 1) {
      setReport1(file);
    } else {
      setReport2(file);
    }
  };

  const handleDrop = (e, fileNum) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFileSelect(fileNum, file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const compareReports = async () => {
    if (!report1 || !report2) {
      setError('Please upload both reports');
      return;
    }

    setComparing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('report1', report1);
      formData.append('report2', report2);

      const response = await reportAPI.compareReports(formData);
      setComparisonData(response.data);
    } catch (err) {
      console.error('Comparison error:', err);
      setError('Failed to compare reports. Please try again.');
    } finally {
      setComparing(false);
    }
  };

  const resetComparison = () => {
    setReport1(null);
    setReport2(null);
    setComparisonData(null);
    setError('');
  };

  const getChangeIcon = (change) => {
    if (change > 0) return '↑';
    if (change < 0) return '↓';
    return '→';
  };

  const getChangeColor = (change, testName) => {
    const lowerIsBetter = ['cholesterol', 'ldl', 'triglycerides', 'glucose', 'hba1c'];
    const isLowerBetter = lowerIsBetter.some(t => testName.toLowerCase().includes(t));
    
    if (change > 0) return isLowerBetter ? '#EF4444' : '#10B981';
    if (change < 0) return isLowerBetter ? '#10B981' : '#EF4444';
    return '#6B7280';
  };

  // Render upload interface
  if (!comparisonData) {
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
              <a href="/health" className="nav-link active">Analytics</a>
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

        <div className="health-trends-container">
          {/* Hero Section */}
          <div className="trends-hero">
            <div className="trends-hero-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <h1>Compare Health Reports</h1>
            <p>Upload two medical reports to track your health progress over time</p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="health-alert health-alert-error">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
              </svg>
              {error}
            </div>
          )}

          {/* Upload Grid */}
          <div className="upload-grid">
            {/* Report 1 */}
            <div className="upload-column">
              <div className="upload-column-header">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <span>Report 1 (Older)</span>
              </div>
              <div
                className={`upload-dropzone ${report1 ? 'has-file' : ''}`}
                onDrop={(e) => handleDrop(e, 1)}
                onDragOver={handleDragOver}
                onClick={() => fileInput1Ref.current?.click()}
              >
                {report1 ? (
                  <>
                    <div className="upload-success-icon">
                      <svg width="40" height="40" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                      </svg>
                    </div>
                    <div className="upload-file-name">{report1.name}</div>
                    <div className="upload-file-size">{(report1.size / 1024).toFixed(1)} KB</div>
                  </>
                ) : (
                  <>
                    <div className="upload-dropzone-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <div className="upload-dropzone-text">Drop file here</div>
                    <div className="upload-dropzone-subtext">or click to browse</div>
                  </>
                )}
              </div>
              <input
                ref={fileInput1Ref}
                type="file"
                accept="application/pdf"
                onChange={(e) => handleFileSelect(1, e.target.files[0])}
                style={{ display: 'none' }}
              />
            </div>

            {/* VS Divider */}
            <div className="vs-divider">
              <div className="vs-circle">VS</div>
            </div>

            {/* Report 2 */}
            <div className="upload-column">
              <div className="upload-column-header">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <span>Report 2 (Newer)</span>
              </div>
              <div
                className={`upload-dropzone ${report2 ? 'has-file' : ''}`}
                onDrop={(e) => handleDrop(e, 2)}
                onDragOver={handleDragOver}
                onClick={() => fileInput2Ref.current?.click()}
              >
                {report2 ? (
                  <>
                    <div className="upload-success-icon">
                      <svg width="40" height="40" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                      </svg>
                    </div>
                    <div className="upload-file-name">{report2.name}</div>
                    <div className="upload-file-size">{(report2.size / 1024).toFixed(1)} KB</div>
                  </>
                ) : (
                  <>
                    <div className="upload-dropzone-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <div className="upload-dropzone-text">Drop file here</div>
                    <div className="upload-dropzone-subtext">or click to browse</div>
                  </>
                )}
              </div>
              <input
                ref={fileInput2Ref}
                type="file"
                accept="application/pdf"
                onChange={(e) => handleFileSelect(2, e.target.files[0])}
                style={{ display: 'none' }}
              />
            </div>
          </div>

          {/* Compare Button */}
          <div className="compare-button-wrapper">
            <button
              onClick={compareReports}
              disabled={!report1 || !report2 || comparing}
              className="btn-compare-reports"
            >
              {comparing ? (
                <>
                  <span className="button-spinner"></span>
                  Comparing Reports...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd"/>
                  </svg>
                  Compare Reports
                </>
              )}
            </button>
          </div>

          {/* Info Card */}
          <div className="info-card">
            <div className="info-card-header">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
              </svg>
              <span>How it works</span>
            </div>
            <ul className="info-list">
              <li>Upload your older medical report as Report 1</li>
              <li>Upload your newer medical report as Report 2</li>
              <li>Click "Compare Reports" to analyze the changes</li>
              <li>View visual comparisons and percentage changes</li>
              <li>Track your health progress over time</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Results view - continuing below due to size
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
            <a href="/health" className="nav-link active">Analytics</a>
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

      <div className="health-trends-container">
        {/* Results Header */}
        <div className="results-header">
          <h1>Health Comparison Results</h1>
          <button onClick={resetComparison} className="btn-secondary-action">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd"/>
            </svg>
            New Comparison
          </button>
        </div>

        {/* Report Dates */}
        <div className="report-dates-grid">
          <div className="report-date-card">
            <span className="report-date-label">Report 1 (Older)</span>
            <span className="report-date-value">
              {comparisonData.report1_date ? new Date(comparisonData.report1_date).toLocaleDateString('en-GB') : 'Date N/A'}
            </span>
          </div>
          <div className="report-date-card">
            <span className="report-date-label">Report 2 (Newer)</span>
            <span className="report-date-value">
              {comparisonData.report2_date ? new Date(comparisonData.report2_date).toLocaleDateString('en-GB') : 'Date N/A'}
            </span>
          </div>
        </div>

        {/* Summary Card */}
        {comparisonData.summary && (
          <div className="summary-card">
            <div className="summary-header">
              <div className="summary-icon">
                {comparisonData.summary.improved_count > comparisonData.summary.worsened_count ? (
                  <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                  </svg>
                ) : (
                  <svg width="32" height="32" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                  </svg>
                )}
              </div>
              <h2>Overall Health Summary</h2>
            </div>
            <div className="summary-stats">
              <div className="summary-stat improved">
                <div className="stat-value">{comparisonData.summary.improved_count}</div>
                <div className="stat-label">Tests Improved</div>
              </div>
              <div className="summary-stat worsened">
                <div className="stat-value">{comparisonData.summary.worsened_count}</div>
                <div className="stat-label">Tests Worsened</div>
              </div>
              <div className="summary-stat stable">
                <div className="stat-value">{comparisonData.summary.stable_count}</div>
                <div className="stat-label">Tests Stable</div>
              </div>
            </div>
          </div>
        )}

        {/* Comparison Table */}
        {comparisonData.comparisons && comparisonData.comparisons.length > 0 ? (
          <>
            <div className="section-title-wrapper">
              <h2>Test-by-Test Comparison</h2>
            </div>
            
            <div className="comparison-table-wrapper">
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th>Test Name</th>
                    <th>Report 1</th>
                    <th>Report 2</th>
                    <th>Change</th>
                    <th>%</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonData.comparisons.map((test, index) => {
                    const change = test.value2 - test.value1;
                    const percentChange = test.value1 !== 0 ? ((change / test.value1) * 100).toFixed(1) : 'N/A';
                    const changeColor = getChangeColor(change, test.name);
                    
                    return (
                      <tr key={index}>
                        <td className="test-name">{test.name}</td>
                        <td>{test.value1} {test.unit}</td>
                        <td>{test.value2} {test.unit}</td>
                        <td style={{ color: changeColor, fontWeight: 600 }}>
                          {getChangeIcon(change)} {Math.abs(change).toFixed(2)} {test.unit}
                        </td>
                        <td style={{ color: changeColor, fontWeight: 600 }}>
                          {percentChange !== 'N/A' ? `${percentChange}%` : 'N/A'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Visual Charts */}
            <div className="section-title-wrapper">
              <h2>Visual Comparison</h2>
            </div>
            
            <div className="charts-grid">
              {comparisonData.comparisons.slice(0, 6).map((test, index) => {
                const chartData = {
                  labels: ['Report 1', 'Report 2'],
                  datasets: [{
                    label: `${test.name} (${test.unit})`,
                    data: [test.value1, test.value2],
                    backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(16, 185, 129, 0.8)'],
                    borderColor: ['#3B82F6', '#10B981'],
                    borderWidth: 2,
                    borderRadius: 8
                  }]
                };

                return (
                  <div key={index} className="chart-card">
                    <h4>{test.name}</h4>
                    <div className="chart-wrapper">
                      <Bar
                        data={chartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          plugins: {
                            legend: { display: false },
                            tooltip: {
                              callbacks: {
                                label: (context) => `${context.parsed.y} ${test.unit}`
                              }
                            }
                          },
                          scales: {
                            y: {
                              beginAtZero: false,
                              grid: { color: '#E5E7EB' },
                              ticks: {
                                callback: (value) => `${value} ${test.unit}`
                              }
                            },
                            x: { grid: { display: false } }
                          }
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <div className="modern-empty-state">
            <div className="empty-icon-wrapper">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <h3>No Matching Tests Found</h3>
            <p>Make sure both reports contain similar test results for comparison</p>
            <button onClick={resetComparison} className="btn-get-started">
              Try Different Reports
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default HealthTrends;