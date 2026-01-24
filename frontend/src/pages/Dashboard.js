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
  const [processingStage, setProcessingStage] = useState(''); // NEW: Track processing stage
  const [useAI, setUseAI] = useState(false);
  const [verifyReport, setVerifyReport] = useState(false);
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

    // Simulated progress stages
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
      
      // Wait a bit to show success message
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
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Medical Report Summarizer</h1>
        <div className="user-info">
          <span>Welcome, {username}!</span>
          <button onClick={toggleDarkMode} className="btn-secondary" style={{ marginRight: '12px' }}>
            {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
          </button>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>

      <div className="upload-section">
        <h2>Upload New Report</h2>
        
        {/* AI Toggle */}
        <div style={{
          marginBottom: '20px',
          padding: '16px',
          background: 'var(--bg-gray)',
          borderRadius: '12px',
          border: '2px solid var(--border)',
          transition: 'all 0.3s ease'
        }}>
          <label style={{
            display: 'flex',
            alignItems: 'center',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: '500'
          }}>
            <input
              type="checkbox"
              checked={useAI}
              onChange={(e) => setUseAI(e.target.checked)}
              style={{
                width: '20px',
                height: '20px',
                marginRight: '12px',
                cursor: 'pointer'
              }}
            />
            <div>
              <span style={{ color: 'var(--text-primary)' }}>
                🤖 Enhance with AI (Gemini)
              </span>
              <div style={{
                fontSize: '14px',
                color: 'var(--text-secondary)',
                marginTop: '4px'
              }}>
                Adds conversational polish to the rule-based summary. 
                {useAI ? ' AI enhancement enabled' : ' Pure rule-based analysis (faster)'}
              </div>
            </div>
          </label>
        </div>

        {/* Verification Toggle */}
        <div style={{
          marginBottom: '20px',
          padding: '16px',
          background: 'var(--bg-gray)',
          borderRadius: '12px',
          border: '2px solid var(--border)',
          transition: 'all 0.3s ease'
        }}>
          <label style={{
            display: 'flex',
            alignItems: 'center',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: '500'
          }}>
            <input
              type="checkbox"
              checked={verifyReport}
              onChange={(e) => setVerifyReport(e.target.checked)}
              style={{
                width: '20px',
                height: '20px',
                marginRight: '12px',
                cursor: 'pointer'
              }}
            />
            <div>
              <span style={{ color: 'var(--text-primary)' }}>
                🔍 Verify Report Authenticity
              </span>
              <div style={{
                fontSize: '14px',
                color: 'var(--text-secondary)',
                marginTop: '4px'
              }}>
                Checks for tampering, editing, or fake reports. Use if suspicious.
                {verifyReport ? ' Verification enabled' : ' (Optional)'}
              </div>
            </div>
          </label>
        </div>

        <div
          className={`upload-box ${isDragging ? 'drag-over' : ''}`}
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
            <>
              <span className="upload-icon">📄</span>
              <h3>Drop document here to upload</h3>
              <p className="file-types">
                Up to 50MB for PDF • Up to 5MB for images (JPG, PNG)
              </p>
              <button
                className="btn-select-file"
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
                disabled={uploading}
              >
                Select a document
              </button>
            </>
          ) : (
            <div className="selected-file" onClick={(e) => e.stopPropagation()}>
              <div className="selected-file-name">
                <span>📄</span>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                  <span>{selectedFile.name}</span>
                  {fileSize && (
                    <span style={{ 
                      fontSize: '13px', 
                      color: 'var(--text-secondary)',
                      marginTop: '4px'
                    }}>
                      {formatFileSize(fileSize)}
                    </span>
                  )}
                </div>
              </div>
              {!uploading && (
                <button className="btn-remove-file" onClick={handleRemoveFile}>×</button>
              )}
            </div>
          )}
        </div>

        {selectedFile && !uploading && (
          <button onClick={handleUpload} className="btn-upload">
            {`Upload & ${useAI ? 'Analyze with AI' : 'Analyze'}`}
          </button>
        )}

        {uploading && (
          <div className="upload-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${uploadProgress}%` }}></div>
            </div>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              gap: '12px',
              marginTop: '12px'
            }}>
              <div className="dots-loader">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p style={{ margin: 0 }}>{processingStage}</p>
            </div>
            <p style={{ 
              textAlign: 'center', 
              fontSize: '13px', 
              color: 'var(--text-secondary)',
              marginTop: '8px'
            }}>
              {uploadProgress}% complete
            </p>
          </div>
        )}

        {uploadError && <div className="error-message">{uploadError}</div>}
        {uploadSuccess && <div className="success-message">{uploadSuccess}</div>}
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-cards">
          <div className="action-card" onClick={() => navigate('/history')}>
            <h3>📜 View History</h3>
            <p>See all your uploaded reports</p>
            <span className="action-arrow">→</span>
          </div>
          
          <div className="action-card" onClick={() => navigate('/health')}>
            <h3>📊 Health Trends</h3>
            <p>Track your health over time</p>
            <span className="action-arrow">→</span>
          </div>

          <div className="action-card" onClick={() => navigate('/jargon')}>
            <h3>💡 Jargon Buster</h3>
            <p>Understand medical terms</p>
            <span className="action-arrow">→</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;