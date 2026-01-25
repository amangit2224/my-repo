import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { reportAPI, getApiErrorMessage } from '../utils/api';
import '../App.css';

function Dashboard({ darkMode, setDarkMode }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileSize, setFileSize] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [processingStage, setProcessingStage] = useState('');
  const [useAI, setUseAI] = useState(false);
  const [verifyReport, setVerifyReport] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  // Get greeting based on time
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

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

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const validateFile = (file) => {
    const isPDF = file.type === 'application/pdf';
    const isImage = file.type.startsWith('image/');
    const sizeMB = file.size / (1024 * 1024);
    const sizeFormatted = formatFileSize(file.size);

    if (!isPDF && !isImage) {
      return {
        valid: false,
        error: `Invalid file type. Only PDF, JPG, and PNG files are allowed.`,
        details: `You uploaded: ${file.type || 'unknown type'}`
      };
    }

    if (isPDF && sizeMB > 50) {
      return {
        valid: false,
        error: `PDF file is too large (${sizeFormatted})`,
        details: `Maximum size for PDFs is 50 MB. Please compress your PDF or split it into smaller files.`
      };
    }

    if (isImage && sizeMB > 5) {
      return {
        valid: false,
        error: `Image file is too large (${sizeFormatted})`,
        details: `Maximum size for images is 5 MB. Please compress your image before uploading.`
      };
    }

    return {
      valid: true,
      error: null,
      details: null
    };
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const validation = validateFile(file);
      
      if (!validation.valid) {
        setUploadError(validation.error);
        setSelectedFile(null);
        setFileSize(null);
        
        if (validation.details) {
          setTimeout(() => {
            setUploadError(validation.details);
          }, 100);
        }
        return;
      }
      
      setSelectedFile(file);
      setFileSize(file.size);
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
      const validation = validateFile(files[0]);
      
      if (!validation.valid) {
        setUploadError(validation.error);
        setSelectedFile(null);
        setFileSize(null);
        
        if (validation.details) {
          setTimeout(() => {
            setUploadError(validation.details);
          }, 2000);
        }
        return;
      }
      
      setSelectedFile(files[0]);
      setFileSize(files[0].size);
      setUploadError('');
      setUploadSuccess('');
    }
  };

  const handleRemoveFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setFileSize(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const validation = validateFile(selectedFile);
    if (!validation.valid) {
      setUploadError(validation.error);
      return;
    }

    setUploading(true);
    setUploadError('');
    setUploadSuccess('');
    setUploadProgress(0);
    setProcessingStage('Uploading file...');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('use_ai', useAI);
    formData.append('verify_report', verifyReport);

    const stages = [
      { progress: 20, message: 'Uploading file...' },
      { progress: 40, message: 'Extracting text...' },
      { progress: 60, message: verifyReport ? 'Verifying authenticity...' : 'Analyzing report...' },
      { progress: 80, message: useAI ? 'Enhancing with AI...' : 'Generating summary...' },
      { progress: 90, message: 'Almost done...' }
    ];

    let currentStage = 0;
    const interval = setInterval(() => {
      if (currentStage < stages.length) {
        setUploadProgress(stages[currentStage].progress);
        setProcessingStage(stages[currentStage].message);
        currentStage++;
      }
    }, 1000);

    try {
      const response = await reportAPI.upload(formData);
      
      clearInterval(interval);
      setUploadProgress(100);
      setProcessingStage('Complete!');
      
      const method = response.data.method_used || response.data.method || 'unknown';
      const methodText = method === 'rule_based_only' ? 'Rule-based analysis' : 
                        method === 'rule_based_with_ai' ? 'Rule-based + AI enhancement' : 
                        'AI analysis';
      
      let successMessage = `Report processed successfully using ${methodText}!`;
      if (response.data.verification_enabled) {
        successMessage += ' Verification completed.';
      }
      
      setUploadSuccess(successMessage);
      
      setTimeout(() => {
        setSelectedFile(null);
        setFileSize(null);
        setUseAI(false);
        setVerifyReport(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
        
        const reportId = response.data.report_id;
        
        if (reportId && reportId !== 'undefined') {
          navigate(`/report/${reportId}`);
          setTimeout(() => fetchReports(), 1000);
        } else {
          setUploadError('Upload successful but navigation failed');
          fetchReports();
        }
      }, 1500);
      
    } catch (error) {
      clearInterval(interval);
      console.error('Upload error:', error);
      
      const errorMessage = getApiErrorMessage(error);
      setUploadError(errorMessage);
      setProcessingStage('');
      
    } finally {
      setTimeout(() => {
        setUploading(false);
        setUploadProgress(0);
        setProcessingStage('');
      }, 1500);
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
    <div className="dashboard-wrapper">
      {/* Modern Navbar */}
      <nav className="modern-navbar">
        <div className="navbar-content">
          {/* Logo */}
          <div className="navbar-logo">
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

          {/* Nav Links */}
          <div className="navbar-links">
            <a href="/dashboard" className="nav-link active">Dashboard</a>
            <a href="/history" className="nav-link">History</a>
            <a href="/health" className="nav-link">Analytics</a>
          </div>

          {/* Right Section */}
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

      <div className="dashboard-container">
        {/* Greeting Section */}
        <div className="greeting-section">
          <div>
            <h1 className="greeting-title">{getGreeting()}, {username}!</h1>
            <p className="greeting-subtitle">Ready to analyze your medical reports</p>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="dashboard-grid">
          {/* Upload Section */}
          <div className="upload-card">
            <div className="card-header">
              <h2>Upload New Report</h2>
              <p>Drag and drop or click to select</p>
            </div>
            
            {/* AI & Verification Options */}
            <div className="options-grid">
              <label className="option-card">
                <input
                  type="checkbox"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  className="option-checkbox"
                />
                <div className="option-icon ai-icon">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13 7H7v6h6V7z"/>
                    <path fillRule="evenodd" d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v2h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1H9v1a1 1 0 11-2 0v-1H5a2 2 0 01-2-2v-2H2a1 1 0 110-2h1V9H2a1 1 0 010-2h1V5a2 2 0 012-2h2V2zM5 5h10v10H5V5z" clipRule="evenodd"/>
                  </svg>
                </div>
                <div className="option-content">
                  <span className="option-title">AI Enhancement</span>
                  <span className="option-desc">Polish with Gemini AI</span>
                </div>
              </label>

              <label className="option-card">
                <input
                  type="checkbox"
                  checked={verifyReport}
                  onChange={(e) => setVerifyReport(e.target.checked)}
                  className="option-checkbox"
                />
                <div className="option-icon verify-icon">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                  </svg>
                </div>
                <div className="option-content">
                  <span className="option-title">Verify Authenticity</span>
                  <span className="option-desc">Check for tampering</span>
                </div>
              </label>
            </div>

            {/* Upload Box */}
            <div
              className={`modern-upload-box ${isDragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => !uploading && fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileChange}
                disabled={uploading}
                style={{ display: 'none' }}
              />

              {!selectedFile ? (
                <div className="upload-empty-state">
                  <div className="upload-icon-wrapper">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                    </svg>
                  </div>
                  <h3>Drop your file here</h3>
                  <p>or click to browse</p>
                  <div className="file-requirements">
                    <span>PDF up to 50MB</span>
                    <span>•</span>
                    <span>Images up to 5MB</span>
                  </div>
                </div>
              ) : (
                <div className="file-selected" onClick={(e) => e.stopPropagation()}>
                  <div className="file-icon">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <div className="file-info">
                    <span className="file-name">{selectedFile.name}</span>
                    <span className="file-size">{formatFileSize(fileSize)}</span>
                  </div>
                  {!uploading && (
                    <button className="file-remove-btn" onClick={handleRemoveFile}>
                      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"/>
                      </svg>
                    </button>
                  )}
                </div>
              )}
            </div>

            {selectedFile && !uploading && (
              <button onClick={handleUpload} className="upload-submit-btn">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd"/>
                </svg>
                {`Upload & ${useAI ? 'Analyze with AI' : 'Analyze'}`}
              </button>
            )}

            {uploading && (
              <div className="modern-upload-progress">
                <div className="progress-track">
                  <div className="progress-bar-fill" style={{ width: `${uploadProgress}%` }}></div>
                </div>
                <div className="progress-info">
                  <span className="progress-stage">{processingStage}</span>
                  <span className="progress-percent">{uploadProgress}%</span>
                </div>
              </div>
            )}

            {uploadError && (
              <div className="alert alert-error">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                </svg>
                {uploadError}
              </div>
            )}
            {uploadSuccess && (
              <div className="alert alert-success">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
                {uploadSuccess}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="quick-actions-grid">
            <h2 className="section-title">Quick Actions</h2>
            
            <div className="action-card-modern" onClick={() => navigate('/history')}>
              <div className="action-icon-wrapper history-gradient">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>View History</h3>
                <p>See all your uploaded reports</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>

            <div className="action-card-modern" onClick={() => navigate('/health')}>
              <div className="action-icon-wrapper health-gradient">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>Health Trends</h3>
                <p>Track your health over time</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>

            <div className="action-card-modern" onClick={() => navigate('/jargon')}>
              <div className="action-icon-wrapper jargon-gradient">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div className="action-card-content">
                <h3>Jargon Buster</h3>
                <p>Understand medical terms</p>
              </div>
              <div className="action-arrow">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;