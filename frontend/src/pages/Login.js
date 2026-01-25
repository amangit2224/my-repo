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
                <rect width="48" height="48" rx="12" fill="url(#logoGradient)"/>
                <path d="M24 14L16 20V32L24 38L32 32V20L24 14Z" fill="white" fillOpacity="0.9"/>
                <path d="M24 20V32M20 24H28M20 28H28" stroke="url(#logoGradient)" strokeWidth="2" strokeLinecap="round"/>
                <defs>
                  <linearGradient id="logoGradient" x1="0" y1="0" x2="48" y2="48">
                    <stop offset="0%" stopColor="#2563EB"/>
                    <stop offset="100%" stopColor="#7C3AED"/>
                  </linearGradient>
                </defs>
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
              Securely Upload And Store<br />
              Your Important Documents<br />
              With <span className="hero-brand">MedLens!</span>
            </h2>
            
            {/* Illustration */}
            <div className="hero-illustration">
              <svg viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Decorative dots */}
                <g opacity="0.3">
                  <circle cx="280" cy="150" r="3" fill="#CBD5E1"/>
                  <circle cx="295" cy="150" r="3" fill="#CBD5E1"/>
                  <circle cx="310" cy="150" r="3" fill="#CBD5E1"/>
                  <circle cx="280" cy="165" r="3" fill="#CBD5E1"/>
                  <circle cx="295" cy="165" r="3" fill="#CBD5E1"/>
                  <circle cx="310" cy="165" r="3" fill="#CBD5E1"/>
                  <circle cx="280" cy="180" r="3" fill="#CBD5E1"/>
                  <circle cx="295" cy="180" r="3" fill="#CBD5E1"/>
                  <circle cx="310" cy="180" r="3" fill="#CBD5E1"/>
                </g>
                
                {/* Curved line decoration */}
                <path d="M 450 100 Q 520 150 480 250" stroke="#CBD5E1" strokeWidth="2" fill="none" opacity="0.3"/>
                
                {/* Main character blob */}
                <ellipse cx="300" cy="250" rx="140" ry="100" fill="url(#blobGradient)"/>
                
                {/* Head */}
                <circle cx="300" cy="170" r="35" fill="white"/>
                
                {/* Laptop */}
                <rect x="270" y="215" width="60" height="40" rx="3" fill="#E0F2FE"/>
                <rect x="265" y="255" width="70" height="3" fill="#64748B"/>
                
                {/* Arms */}
                <path d="M 240 220 Q 230 240 250 250" stroke="#1E293B" strokeWidth="8" strokeLinecap="round"/>
                <path d="M 360 220 Q 370 240 350 250" stroke="#1E293B" strokeWidth="8" strokeLinecap="round"/>
                
                {/* Legs */}
                <line x1="280" y1="320" x2="280" y2="360" stroke="#1E293B" strokeWidth="8" strokeLinecap="round"/>
                <line x1="320" y1="320" x2="320" y2="360" stroke="#1E293B" strokeWidth="8" strokeLinecap="round"/>
                
                {/* Ground */}
                <line x1="200" y1="360" x2="400" y2="360" stroke="#1E293B" strokeWidth="3" strokeLinecap="round"/>
                
                <defs>
                  <linearGradient id="blobGradient" x1="200" y1="150" x2="400" y2="350">
                    <stop offset="0%" stopColor="#60A5FA"/>
                    <stop offset="50%" stopColor="#34D399"/>
                    <stop offset="100%" stopColor="#60A5FA"/>
                  </linearGradient>
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