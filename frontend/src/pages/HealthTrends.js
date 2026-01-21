// src/pages/HealthTrends.js
// 🔥 NEW HEALTH TRENDS - Compare 2 Reports Side-by-Side!
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

function HealthTrends() {
  const navigate = useNavigate();
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

  const handleFileSelect = (fileNum, file) => {
    if (!file) return;
    
    // Validate file type
    if (file.type !== 'application/pdf') {
      setError('Please upload PDF files only');
      return;
    }
    
    // Validate file size (max 10MB)
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

      // Use your existing API utility
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
    // For some tests, increase is bad (e.g., cholesterol, glucose)
    const lowerIsBetter = ['cholesterol', 'ldl', 'triglycerides', 'glucose', 'hba1c'];
    const isLowerBetter = lowerIsBetter.some(t => testName.toLowerCase().includes(t));
    
    if (change > 0) return isLowerBetter ? '#EF4444' : '#10B981'; // Red or Green
    if (change < 0) return isLowerBetter ? '#10B981' : '#EF4444'; // Green or Red
    return '#6B7280'; // Gray
  };

  // Render upload interface
  if (!comparisonData) {
    return (
      <div className="dashboard-container">
        {/* Header */}
        <div className="dashboard-header">
          <h1>📊 Health Trends - Compare Reports</h1>
          <div className="user-info">
            <button onClick={() => navigate('/dashboard')} className="btn-secondary">
              Back
            </button>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>

        {/* Upload Section */}
        <div className="upload-section" style={{ padding: 32, maxWidth: 1000, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <h2 style={{ marginBottom: 12, fontSize: 24 }}>Compare Your Health Reports</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: 16 }}>
              Upload two medical reports to see how your health has changed over time
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div style={{
              padding: 16,
              background: '#FEE2E2',
              border: '1px solid #EF4444',
              borderRadius: 8,
              color: '#DC2626',
              marginBottom: 24,
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}

          {/* Upload Boxes */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 24,
            marginBottom: 32
          }}>
            {/* Report 1 Upload */}
            <div>
              <h3 style={{ fontSize: 16, marginBottom: 12, color: 'var(--text-primary)' }}>
                📄 Report 1 (Older)
              </h3>
              <div
                onDrop={(e) => handleDrop(e, 1)}
                onDragOver={handleDragOver}
                onClick={() => fileInput1Ref.current?.click()}
                style={{
                  border: '2px dashed var(--primary)',
                  borderRadius: 12,
                  padding: 40,
                  textAlign: 'center',
                  cursor: 'pointer',
                  background: report1 ? 'var(--primary-light)' : 'var(--bg-gray)',
                  transition: 'all 0.3s'
                }}
              >
                {report1 ? (
                  <>
                    <div style={{ fontSize: 48, marginBottom: 8 }}>✅</div>
                    <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: 4 }}>
                      {report1.name}
                    </div>
                    <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
                      {(report1.size / 1024).toFixed(1)} KB
                    </div>
                  </>
                ) : (
                  <>
                    <div style={{ fontSize: 48, marginBottom: 8 }}>📄</div>
                    <div style={{ fontWeight: 600, marginBottom: 4 }}>Drop file here</div>
                    <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
                      or click to browse
                    </div>
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

            {/* Report 2 Upload */}
            <div>
              <h3 style={{ fontSize: 16, marginBottom: 12, color: 'var(--text-primary)' }}>
                📄 Report 2 (Newer)
              </h3>
              <div
                onDrop={(e) => handleDrop(e, 2)}
                onDragOver={handleDragOver}
                onClick={() => fileInput2Ref.current?.click()}
                style={{
                  border: '2px dashed var(--primary)',
                  borderRadius: 12,
                  padding: 40,
                  textAlign: 'center',
                  cursor: 'pointer',
                  background: report2 ? 'var(--primary-light)' : 'var(--bg-gray)',
                  transition: 'all 0.3s'
                }}
              >
                {report2 ? (
                  <>
                    <div style={{ fontSize: 48, marginBottom: 8 }}>✅</div>
                    <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: 4 }}>
                      {report2.name}
                    </div>
                    <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
                      {(report2.size / 1024).toFixed(1)} KB
                    </div>
                  </>
                ) : (
                  <>
                    <div style={{ fontSize: 48, marginBottom: 8 }}>📄</div>
                    <div style={{ fontWeight: 600, marginBottom: 4 }}>Drop file here</div>
                    <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
                      or click to browse
                    </div>
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
          <div style={{ textAlign: 'center' }}>
            <button
              onClick={compareReports}
              disabled={!report1 || !report2 || comparing}
              className="btn-primary"
              style={{
                padding: '16px 48px',
                fontSize: 16,
                opacity: (!report1 || !report2 || comparing) ? 0.5 : 1,
                cursor: (!report1 || !report2 || comparing) ? 'not-allowed' : 'pointer'
              }}
            >
              {comparing ? (
                <>
                  <span className="spinner" style={{ marginRight: 8 }}></span>
                  Comparing Reports...
                </>
              ) : (
                '🔍 Compare Reports'
              )}
            </button>
          </div>

          {/* Info Box */}
          <div style={{
            marginTop: 40,
            padding: 24,
            background: 'var(--bg-gray)',
            borderRadius: 12,
            border: '1px solid #E5E7EB'
          }}>
            <h4 style={{ fontSize: 16, marginBottom: 12 }}>💡 How it works:</h4>
            <ul style={{ paddingLeft: 20, color: 'var(--text-secondary)', lineHeight: 1.8 }}>
              <li>Upload your older medical report as Report 1</li>
              <li>Upload your newer medical report as Report 2</li>
              <li>Click "Compare Reports" to see the changes</li>
              <li>View visual comparisons of all your test results</li>
              <li>See percentage changes and health trends</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Render comparison results
  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <h1>📈 Health Comparison Results</h1>
        <div className="user-info">
          <button onClick={resetComparison} className="btn-secondary">
            New Comparison
          </button>
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            Dashboard
          </button>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>

      {/* Results Section */}
      <div className="upload-section" style={{ padding: 32, maxWidth: 1200, margin: '0 auto' }}>
        {/* Report Info */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 24,
          marginBottom: 32
        }}>
          <div style={{
            padding: 20,
            background: 'var(--bg-gray)',
            borderRadius: 12,
            border: '2px solid var(--primary)'
          }}>
            <h3 style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 8 }}>
              📄 Report 1 (Older)
            </h3>
            <div style={{ fontWeight: 600, fontSize: 16, color: 'var(--text-primary)' }}>
              {comparisonData.report1_date ? new Date(comparisonData.report1_date).toLocaleDateString('en-GB') : 'Date N/A'}
            </div>
          </div>
          <div style={{
            padding: 20,
            background: 'var(--bg-gray)',
            borderRadius: 12,
            border: '2px solid var(--primary)'
          }}>
            <h3 style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 8 }}>
              📄 Report 2 (Newer)
            </h3>
            <div style={{ fontWeight: 600, fontSize: 16, color: 'var(--text-primary)' }}>
              {comparisonData.report2_date ? new Date(comparisonData.report2_date).toLocaleDateString('en-GB') : 'Date N/A'}
            </div>
          </div>
        </div>

        {/* Overall Summary */}
        {comparisonData.summary && (
          <div style={{
            padding: 24,
            background: 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
            borderRadius: 16,
            marginBottom: 32,
            color: 'white',
            textAlign: 'center'
          }}>
            <h2 style={{ fontSize: 24, marginBottom: 12 }}>
              {comparisonData.summary.improved_count > comparisonData.summary.worsened_count ? '🎉' : '⚠️'}
              {' '}Overall Health Summary
            </h2>
            <div style={{ fontSize: 18, opacity: 0.9 }}>
              <strong>{comparisonData.summary.improved_count}</strong> tests improved • 
              <strong> {comparisonData.summary.worsened_count}</strong> tests worsened • 
              <strong> {comparisonData.summary.stable_count}</strong> stable
            </div>
          </div>
        )}

        {/* Comparison Table */}
        {comparisonData.comparisons && comparisonData.comparisons.length > 0 && (
          <div style={{ marginBottom: 40 }}>
            <h3 style={{ fontSize: 20, marginBottom: 20, fontWeight: 600 }}>
              📊 Test-by-Test Comparison
            </h3>
            <div style={{
              background: 'white',
              borderRadius: 12,
              overflow: 'hidden',
              boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-gray)' }}>
                    <th style={{ padding: 16, textAlign: 'left', fontWeight: 600 }}>Test Name</th>
                    <th style={{ padding: 16, textAlign: 'center', fontWeight: 600 }}>Report 1</th>
                    <th style={{ padding: 16, textAlign: 'center', fontWeight: 600 }}>Report 2</th>
                    <th style={{ padding: 16, textAlign: 'center', fontWeight: 600 }}>Change</th>
                    <th style={{ padding: 16, textAlign: 'center', fontWeight: 600 }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonData.comparisons.map((test, index) => {
                    const change = test.value2 - test.value1;
                    const percentChange = test.value1 !== 0 ? ((change / test.value1) * 100).toFixed(1) : 'N/A';
                    const changeColor = getChangeColor(change, test.name);
                    
                    return (
                      <tr key={index} style={{ borderBottom: '1px solid #E5E7EB' }}>
                        <td style={{ padding: 16, fontWeight: 600 }}>{test.name}</td>
                        <td style={{ padding: 16, textAlign: 'center' }}>
                          {test.value1} {test.unit}
                        </td>
                        <td style={{ padding: 16, textAlign: 'center' }}>
                          {test.value2} {test.unit}
                        </td>
                        <td style={{
                          padding: 16,
                          textAlign: 'center',
                          color: changeColor,
                          fontWeight: 600
                        }}>
                          {getChangeIcon(change)} {Math.abs(change).toFixed(2)} {test.unit}
                        </td>
                        <td style={{
                          padding: 16,
                          textAlign: 'center',
                          color: changeColor,
                          fontWeight: 600
                        }}>
                          {percentChange !== 'N/A' ? `${percentChange}%` : 'N/A'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Visual Charts */}
        {comparisonData.comparisons && comparisonData.comparisons.length > 0 && (
          <div>
            <h3 style={{ fontSize: 20, marginBottom: 20, fontWeight: 600 }}>
              📉 Visual Comparison
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
              gap: 24
            }}>
              {comparisonData.comparisons.slice(0, 6).map((test, index) => {
                const chartData = {
                  labels: ['Report 1', 'Report 2'],
                  datasets: [{
                    label: `${test.name} (${test.unit})`,
                    data: [test.value1, test.value2],
                    backgroundColor: [
                      'rgba(79, 70, 229, 0.8)',
                      'rgba(147, 51, 234, 0.8)'
                    ],
                    borderColor: [
                      '#4F46E5',
                      '#9333EA'
                    ],
                    borderWidth: 2
                  }]
                };

                return (
                  <div key={index} style={{
                    background: 'white',
                    padding: 24,
                    borderRadius: 12,
                    boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
                  }}>
                    <h4 style={{ marginBottom: 16, fontSize: 16, fontWeight: 600 }}>
                      {test.name}
                    </h4>
                    <div style={{ height: 250 }}>
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
                            x: {
                              grid: { display: false }
                            }
                          }
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* No comparisons found */}
        {(!comparisonData.comparisons || comparisonData.comparisons.length === 0) && (
          <div className="empty-state">
            <span className="empty-icon">📊</span>
            <p>No matching tests found between the reports</p>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
              Make sure both reports contain similar test results
            </p>
            <button onClick={resetComparison} className="btn-primary">
              Try Different Reports
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default HealthTrends;