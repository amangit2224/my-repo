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

      const testRegex = /\*\*([A-Z][A-Za-z0-9\s\-/()]+?)\*\*:\s*([\d.]+)\s*([a-zA-Z/%]+)/g;
      let match;

      while ((match = testRegex.exec(summary)) !== null) {
        const testName = match[1].trim();
        const value = parseFloat(match[2]);
        const unit = match[3].trim();

        if (!isNaN(value)) {
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

    const testsArray = Object.values(testMap).map(test => {
      test.dataPoints.sort((a, b) => new Date(a.date) - new Date(b.date));
      return test;
    });

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

        const recent = sortedDesc.slice(0, 1);
        setRecentReports(recent);
        extractAllTests(recent);
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
              Showing results from {recentReports.length} report{recentReports.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>

        {/* No tests */}
        {tests.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📊</span>
            <p>No test data found in your most recent report</p>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
              Make sure your latest report contains valid test values
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
