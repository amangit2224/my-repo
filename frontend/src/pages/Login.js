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
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
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
      let errorMessage = getApiErrorMessage(err);
      
      if (err.response?.status === 401) {
        errorMessage = 'Invalid email or password';
      } else if (err.response?.status === 400) {
        errorMessage = 'Please enter both email and password';
      } else if (!err.response) {
        errorMessage = 'Unable to connect. Please check your internet';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Minimal Background Decoration */}
      <div className="login-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      {/* Split Layout Container */}
      <div className="login-split-container">
        {/* Left Side - Login Form */}
        <div className="login-form-side">
          <div className="login-card">
            {/* Logo */}
            <div className="login-logo">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="48" height="48" rx="12" fill="#2563EB"/>
                {/* Document/Report */}
                <rect x="14" y="10" width="20" height="28" rx="2" fill="white"/>
                {/* Scanner lines effect */}
                <line x1="18" y1="16" x2="30" y2="16" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                <line x1="18" y1="20" x2="30" y2="20" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                <line x1="18" y1="24" x2="26" y2="24" stroke="#2563EB" strokeWidth="1.5" strokeLinecap="round"/>
                {/* Medical cross */}
                <circle cx="24" cy="31" r="4" fill="#2563EB"/>
                <path d="M24 29v4M22 31h4" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </div>

            {/* Title */}
            <div className="login-header">
              <h1>Sign in to MedLens</h1>
              <p>Securely analyze and store your medical reports with AI</p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="login-error">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                </svg>
                <span>{error}</span>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="login-form">
              {/* Email Field */}
              <div className="form-field">
                <label htmlFor="email">Email</label>
                <div className="input-wrapper">
                  <svg className="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                  </svg>
                  <input
                    id="email"
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    required
                    autoComplete="email"
                  />
                </div>
              </div>

              {/* Password Field */}
              <div className="form-field">
                <label htmlFor="password">Password</label>
                <div className="input-wrapper">
                  <svg className="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd"/>
                  </svg>
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                    tabIndex="-1"
                  >
                    {showPassword ? (
                      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clipRule="evenodd"/>
                        <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z"/>
                      </svg>
                    ) : (
                      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                        <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd"/>
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              {/* Forgot Password */}
              <div className="form-footer">
                <Link to="/forgot-password" className="forgot-link">
                  Forgot password?
                </Link>
              </div>

              {/* Submit Button */}
              <button type="submit" disabled={loading} className="login-submit">
                {loading ? (
                  <>
                    <span className="button-spinner"></span>
                    Signing in...
                  </>
                ) : (
                  'Get Started'
                )}
              </button>
            </form>

            {/* Sign up link */}
            <div className="login-signup">
              Don't have an account? <Link to="/signup">Sign up</Link>
            </div>
          </div>
        </div>

        {/* Right Side - Hero Section */}
        <div className="login-hero-side">
          <div className="hero-content">
            <h2>
              Securely Upload Your Reports<br />
              And Understand Your Health<br />
              Status With <span className="hero-brand">MedLens!</span>
            </h2>
            
            {/* Illustration */}
            <div className="hero-illustration">
              <svg viewBox="0 0 500 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Background decoration - dots pattern */}
                <g opacity="0.2">
                  <circle cx="100" cy="100" r="2" fill="#64748B"/>
                  <circle cx="110" cy="100" r="2" fill="#64748B"/>
                  <circle cx="120" cy="100" r="2" fill="#64748B"/>
                  <circle cx="130" cy="100" r="2" fill="#64748B"/>
                  <circle cx="100" cy="110" r="2" fill="#64748B"/>
                  <circle cx="110" cy="110" r="2" fill="#64748B"/>
                  <circle cx="120" cy="110" r="2" fill="#64748B"/>
                  <circle cx="130" cy="110" r="2" fill="#64748B"/>
                  <circle cx="100" cy="120" r="2" fill="#64748B"/>
                  <circle cx="110" cy="120" r="2" fill="#64748B"/>
                  <circle cx="120" cy="120" r="2" fill="#64748B"/>
                  <circle cx="130" cy="120" r="2" fill="#64748B"/>
                </g>
                
                {/* Curved decorative line */}
                <path d="M 380 80 Q 420 130 400 200" stroke="#94A3B8" strokeWidth="2" fill="none" opacity="0.3" strokeLinecap="round"/>
                
                {/* Main character body (simplified blob) */}
                <ellipse cx="250" cy="240" rx="110" ry="85" fill="url(#personGradient)" opacity="0.95"/>
                
                {/* Head */}
                <circle cx="250" cy="150" r="32" fill="white"/>
                <circle cx="250" cy="150" r="32" fill="#F1F5F9" opacity="0.5"/>
                
                {/* Laptop/Document */}
                <rect x="225" y="210" width="50" height="35" rx="2" fill="white"/>
                <rect x="227" y="212" width="46" height="31" rx="1" fill="#DBEAFE"/>
                {/* Lines on laptop screen */}
                <line x1="232" y1="220" x2="268" y2="220" stroke="#60A5FA" strokeWidth="2" strokeLinecap="round"/>
                <line x1="232" y1="227" x2="268" y2="227" stroke="#60A5FA" strokeWidth="2" strokeLinecap="round"/>
                <line x1="232" y1="234" x2="255" y2="234" stroke="#60A5FA" strokeWidth="2" strokeLinecap="round"/>
                {/* Laptop base */}
                <rect x="220" y="245" width="60" height="3" rx="1" fill="#94A3B8"/>
                
                {/* Arms (simplified curves) */}
                <path d="M 180 220 Q 170 235 200 245" stroke="#1E293B" strokeWidth="6" strokeLinecap="round" fill="none"/>
                <path d="M 320 220 Q 330 235 300 245" stroke="#1E293B" strokeWidth="6" strokeLinecap="round" fill="none"/>
                
                {/* Legs */}
                <rect x="235" y="310" width="6" height="50" rx="3" fill="#1E293B"/>
                <rect x="259" y="310" width="6" height="50" rx="3" fill="#1E293B"/>
                
                {/* Ground line */}
                <line x1="150" y1="360" x2="350" y2="360" stroke="#1E293B" strokeWidth="3" strokeLinecap="round"/>
                
                {/* Medical report floating beside */}
                <g transform="translate(340, 180)">
                  <rect width="45" height="60" rx="3" fill="white" filter="url(#shadow)"/>
                  <line x1="8" y1="12" x2="37" y2="12" stroke="#60A5FA" strokeWidth="2" strokeLinecap="round"/>
                  <line x1="8" y1="20" x2="37" y2="20" stroke="#60A5FA" strokeWidth="1.5" strokeLinecap="round"/>
                  <line x1="8" y1="27" x2="30" y2="27" stroke="#60A5FA" strokeWidth="1.5" strokeLinecap="round"/>
                  <circle cx="22.5" cy="42" r="8" fill="#34D399"/>
                  <path d="M19 42l2 2 4-4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                </g>
                
                <defs>
                  <linearGradient id="personGradient" x1="150" y1="150" x2="350" y2="330">
                    <stop offset="0%" stopColor="#60A5FA"/>
                    <stop offset="100%" stopColor="#3B82F6"/>
                  </linearGradient>
                  <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                    <feDropShadow dx="0" dy="4" stdDeviation="8" floodOpacity="0.15"/>
                  </filter>
                </defs>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;