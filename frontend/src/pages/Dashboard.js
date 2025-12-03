import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportAPI } from '../utils/api';
import '../App.css';

function Dashboard({ darkMode, setDarkMode }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      await reportAPI.getHistory();
    } catch (error) {
      console.error('Error fetching reports:', error);
    }
  };

  const validateFile = (file) => {
    const isPDF = file.type === 'application/pdf';
    const isImage = file.type.startsWith('image/');
    const sizeMB = file.size / (1024 * 1024);

    if (!isPDF && !isImage) {
      return 'Only PDF, JPG, PNG files are allowed';
    }
    if (isPDF && sizeMB > 10) {
      return 'PDF must be under 10MB';
    }
    if (isImage && sizeMB > 5) {
      return 'Image must be under 5MB';
    }
    return null;
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const error = validateFile(file);
      if (error) {
        setUploadError(error);
        return;
      }
      setSelectedFile(file);
      setUploadError('');
      setUploadSuccess('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const error = validateFile(files[0]);
      if (error) {
        setUploadError(error);
        return;
      }
      setSelectedFile(files[0]);
      setUploadError('');
      setUploadSuccess('');
    }
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadError('');
    setUploadSuccess('');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', selectedFile);

    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) return 90;
        return prev + 15;
      });
    }, 300);

    try {
      const response = await reportAPI.upload(formData);
      setUploadProgress(100);
      setUploadSuccess('Report uploaded and processed successfully!');
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      fetchReports();
      setTimeout(() => navigate(`/report/${response.data.report_id}`), 800);
    } catch (error) {
      setUploadError(error.response?.data?.error || 'Upload failed');
    } finally {
      clearInterval(interval);
      setUploading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Medical Report Summarizer</h1>
        <div className="user-info">
          <span>Welcome, {username}!</span>
          <button onClick={toggleDarkMode} className="btn-secondary" style={{ marginRight: '12px' }}>
            {darkMode ? 'Light Mode' : 'Dark Mode'}
          </button>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>

      <div className="upload-section">
        <h2>Upload New Report</h2>
        <div
          className={`upload-box ${isDragging ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />

          {!selectedFile ? (
            <>
              <span className="upload-icon">Document</span>
              <h3>Drop document here to upload</h3>
              <p className="file-types">
                Up to 10MB for PDF • Up to 5MB for images (JPG, PNG)
              </p>
              <button
                className="btn-select-file"
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
              >
                Select a document
              </button>
            </>
          ) : (
            <div className="selected-file" onClick={(e) => e.stopPropagation()}>
              <div className="selected-file-name">
                <span>Document</span>
                <span>{selectedFile.name}</span>
              </div>
              <button className="btn-remove-file" onClick={handleRemoveFile}>×</button>
            </div>
          )}
        </div>

        {selectedFile && (
          <button onClick={handleUpload} disabled={uploading} className="btn-upload">
            {uploading ? 'Processing...' : 'Upload & Process'}
          </button>
        )}

        {uploading && (
          <div className="upload-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
            </div>
            <p>Analyzing your report...</p>
          </div>
        )}

        {uploadError && <div className="error-message">{uploadError}</div>}
        {uploadSuccess && <div className="success-message">{uploadSuccess}</div>}
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-cards">
          <div className="action-card" onClick={() => navigate('/history')}>
            <h3>View History</h3>
            <p>See all your uploaded reports</p>
            <span className="action-arrow">→</span>
          </div>
          
          <div className="action-card" onClick={() => navigate('/health')}>
            <h3>Health Trends</h3>
            <p>Track your health over time</p>
            <span className="action-arrow">→</span>
        </div>

          <div className="action-card" onClick={() => navigate('/jargon')}>
            <h3>Jargon Buster</h3>
            <p>Understand medical terms</p>
            <span className="action-arrow">→</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
