import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, getApiErrorMessage } from '../utils/api';
import '../App.css';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(formData);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('username', response.data.username);
      navigate('/dashboard');
    } catch (err) {
      // Use enhanced error message from interceptor
      let errorMessage = getApiErrorMessage(err);
      
      // Customize specific login errors
      if (err.response?.status === 401) {
        errorMessage = '🔒 Invalid email or password. Please check your credentials and try again.';
      } else if (err.response?.status === 400) {
        errorMessage = '⚠️ Please enter both email and password.';
      } else if (!err.response) {
        errorMessage = '🌐 Unable to connect. Please check your internet connection.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Medical Report Summarizer</h1>
        <h2>Login</h2>
        
        {error && (
          <div className="error-message" style={{ 
            display: 'flex', 
            alignItems: 'flex-start',
            gap: '8px',
            padding: '12px 16px'
          }}>
            <span>{error}</span>
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your@email.com"
              autoComplete="email"
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
              autoComplete="current-password"
            />
            {/* Forgot Password Link */}
            <div style={{ textAlign: 'right', marginTop: '8px', marginBottom: '12px' }}>
              <Link to="/forgot-password" style={{ fontSize: '14px', color: '#2563eb' }}>
                Forgot Password?
              </Link>
            </div>
          </div>
          
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                <span className="spinner-small"></span>
                Logging in...
              </span>
            ) : (
              'Login'
            )}
          </button>
        </form>
        
        <p className="auth-link">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;