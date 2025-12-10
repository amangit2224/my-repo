// src/pages/HealthTrends.js
import React, { useState, useEffect, useCallback } from 'react';
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
  const [recentReports, setRecentReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tests, setTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState(null);
  const [chartData, setChartData] = useState(null);
  const navigate = useNavigate();

  const handleSelectTest = useCallback((test) => {
    setSelectedTest(test);

    const labels = test.dataPoints.map(dp =>
      new Date(dp.date).toLocaleDateString('en-GB')
    );

    const values = test.dataPoints.map(dp => dp.value);

    setChartData({
      labels,
      datasets: [{
        label: `${test.name} (${test.unit})`,
        data: values,
        backgroundColor: 'rgba(79, 70, 229, 0.9)',
        borderColor: '#4F46E5',
        borderWidth: 1
      }]
    });
  }, []);

  const extractAllTests = useCallback((reportsToAnalyze) => {
    const testMap = {};

    reportsToAnalyze.forEach((report) => {
      const summary = report.plain_language_summary || report.plain_summary || '';
      
      console.log('Analyzing report:', report.filename);
      console.log('Summary preview:', summary.substring(0, 200));

      // FIXED: More flexible regex patterns to catch different formats
      const patterns = [
        // Pattern 1: **Test Name**: value unit
        /\*\*([A-Z][A-Za-z0-9\s\-/()]+?)\*\*:\s*([\d.]+)\s*([a-zA-Z/%]+)/g,
        // Pattern 2: Test Name: value unit (no asterisks)
        /([A-Z][A-Za-z0-9\s\-/()]+?):\s*([\d.]+)\s*([a-zA-Z/%]+)/g,
        // Pattern 3: - Test Name: value unit (bullet points)
        /[-•]\s*([A-Z][A-Za-z0-9\s\-/()]+?):\s*([\d.]+)\s*([a-zA-Z/%]+)/g
      ];

      patterns.forEach(pattern => {
        let match;
        const regexCopy = new RegExp(pattern.source, pattern.flags);
        
        while ((match = regexCopy.exec(summary)) !== null) {
          const testName = match[1].trim();
          const value = parseFloat(match[2]);
          const unit = match[3].trim();

          // Skip if testName is too short or looks like a sentence
          if (testName.length < 3 || testName.split(' ').length > 5) continue;

          if (!isNaN(value)) {
            console.log('Found test:', testName, value, unit);
            
            if (!testMap[testName]) {
              testMap[testName] = {
                name: testName,
                unit,
                dataPoints: []
              };
            }

            testMap[testName].dataPoints.push({
              date: report.uploaded_at,
              value,
              reportId: report.id
            });
          }
        }
      });
    });

    const testsArray = Object.values(testMap).map(test => {
      test.dataPoints.sort((a, b) => new Date(a.date) - new Date(b.date));
      return test;
    });

    console.log('Total tests extracted:', testsArray.length);
    setTests(testsArray);

    if (testsArray.length > 0) {
      handleSelectTest(testsArray[0]);
    } else {
      setSelectedTest(null);
      setChartData(null);
    }
  }, [handleSelectTest]);

  const loadReports = useCallback(async () => {
    setLoading(true);
    try {
      const response = await reportAPI.getHistory();
      const fetchedReports = response.data.reports || [];

      if (fetchedReports.length > 0) {
        const sortedDesc = [...fetchedReports].sort(
          (a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at)
        );

        // FIXED: Analyze ALL reports instead of just 1
        const allReports = sortedDesc.slice(0, 10); // Take up to 10 most recent
        setRecentReports(allReports);
        extractAllTests(allReports);
      } else {
        setRecentReports([]);
        setTests([]);
        setSelectedTest(null);
        setChartData(null);
      }
    } catch (error) {
      console.error('Error loading reports:', error);
    } finally {
      setLoading(false);
    }
  }, [extractAllTests]);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  const getInsight = () => {
    if (!selectedTest || selectedTest.dataPoints.length === 0) return '';

    if (selectedTest.dataPoints.length === 1) {
      const val = selectedTest.dataPoints[0].value;
      return `Latest ${selectedTest.name}: ${val} ${selectedTest.unit}.`;
    }

    const first = selectedTest.dataPoints[0].value;
    const last = selectedTest.dataPoints[selectedTest.dataPoints.length - 1].value;
    const change = last - first;
    const percentChange = first === 0 ? 'N/A' : ((change / first) * 100).toFixed(1);

    const trend =
      change > 0 ? 'increased'
      : change < 0 ? 'decreased'
      : 'no change';

    return `${selectedTest.name} has ${trend} by ${Math.abs(percentChange)}% (from ${first} to ${last} ${selectedTest.unit}).`;
  };

  if (loading) {
    return (
      <div className="loading-state">
        <div className="spinner" />
        <p>Loading your health data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <h1>Health Trends</h1>
        <div className="user-info">
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            Back
          </button>
          <button onClick={() => { localStorage.clear(); navigate('/login'); }} className="btn-logout">
            Logout
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="upload-section" style={{ padding: 32 }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 24
        }}>
          <div>
            <h2 style={{ marginBottom: 8 }}>Your Test Results</h2>
            <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
              Analyzing {recentReports.length} report{recentReports.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>

        {/* No tests */}
        {tests.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📊</span>
            <p>No test data found in your reports</p>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
              Upload medical reports with test values (like blood tests, glucose levels, etc.)
            </p>
            <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 8 }}>
              💡 Tip: Reports should contain values like "Hemoglobin: 14.5 g/dL"
            </p>
            <button onClick={() => navigate('/dashboard')} className="btn-primary">
              Upload Report
            </button>
          </div>
        ) : (
          <>
            {/* Test list */}
            <div style={{ marginBottom: 32 }}>
              <h3 style={{
                fontSize: 16,
                color: 'var(--text-primary)',
                marginBottom: 16,
                fontWeight: 600
              }}>
                Available Tests ({tests.length})
              </h3>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: 12
              }}>
                {tests.map((test, index) => (
                  <div
                    key={index}
                    className="action-card"
                    style={{
                      padding: 16,
                      cursor: 'pointer',
                      border: selectedTest?.name === test.name
                        ? '2px solid var(--primary)'
                        : '2px solid transparent',
                      background: selectedTest?.name === test.name
                        ? 'var(--primary-light)'
                        : 'var(--bg-gray)',
                      transition: 'all 0.2s',
                      textAlign: 'center'
                    }}
                    onClick={() => handleSelectTest(test)}
                  >
                    <div style={{
                      fontWeight: 600,
                      fontSize: 14,
                      marginBottom: 6,
                      color: selectedTest?.name === test.name
                        ? 'var(--primary)'
                        : 'var(--text-primary)'
                    }}>
                      {test.name}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                      {test.dataPoints.length} reading{test.dataPoints.length !== 1 ? 's' : ''}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Chart */}
            {selectedTest && chartData ? (
              <div style={{ maxWidth: 1000, margin: '0 auto' }}>
                <h3 style={{
                  marginBottom: 20,
                  fontSize: 20,
                  fontWeight: 600,
                  color: 'var(--text-primary)'
                }}>
                  {selectedTest.name}
                </h3>

                <div style={{
                  height: 400,
                  background: 'white',
                  padding: 32,
                  borderRadius: 16,
                  marginBottom: 24,
                  boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
                }}>
                  <Bar
                    data={chartData}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: { display: false },
                        tooltip: {
                          callbacks: {
                            label: (context) =>
                              `${context.parsed.y} ${selectedTest.unit}`
                          }
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: false,
                          grid: { color: '#E5E7EB', drawBorder: false },
                          ticks: {
                            callback: (value) => `${value} ${selectedTest.unit}`
                          }
                        },
                        x: {
                          grid: { color: '#E5E7EB', drawBorder: false }
                        }
                      }
                    }}
                  />
                </div>

                {/* Insight */}
                <div style={{
                  padding: 24,
                  background: 'var(--primary-light)',
                  borderRadius: 12,
                  border: '2px solid var(--primary)'
                }}>
                  <strong style={{ fontSize: 18 }}>Insight</strong>
                  <p style={{ marginTop: 12, fontSize: 15 }}>
                    {getInsight()}
                  </p>
                </div>
              </div>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}

export default HealthTrends;