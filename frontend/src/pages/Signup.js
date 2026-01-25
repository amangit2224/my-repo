import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../utils/api';
import '../App.css';

function Signup() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState({
    isValid: false,
    hasLength: false,
    hasUpper: false,
    hasSpecial: false,
    message: ''
  });
  const navigate = useNavigate();

  // Password validation function
  const validatePassword = (password) => {
    const hasLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    const isValid = hasLength && hasUpper && hasSpecial;
    
    let message = '';
    if (!password) {
      message = '';
    } else if (isValid) {
      message = 'Strong password! ✅';
    } else {
      const missing = [];
      if (!hasLength) missing.push('8+ characters');
      if (!hasUpper) missing.push('1 uppercase letter');
      if (!hasSpecial) missing.push('1 special character');
      message = `Need: ${missing.join(', ')}`;
    }
    
    return {
      isValid,
      hasLength,
      hasUpper,
      hasSpecial,
      message
    };
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData({
      ...formData,
      [name]: value,
    });
    
    // Validate password in real-time
    if (name === 'password') {
      const validation = validatePassword(value);
      setPasswordStrength(validation);
    }

    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Check password strength before submitting
    if (!passwordStrength.isValid) {
      setError('Password does not meet security requirements');
      return;
    }
    
    setLoading(true);

    try {
      await authAPI.signup(formData);
      alert('Account created successfully! Please login.');
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.error || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
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

        {/* Header */}
        <div className="login-header">
          <h1>Create Your Account</h1>
          <p>Start analyzing your medical reports with AI</p>
        </div>
        
        {/* Error Message */}
        {error && (
          <div className="error-message">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" style={{ flexShrink: 0 }}>
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
            </svg>
            <span>{error}</span>
          </div>
        )}
        
        {/* Form */}
        <form onSubmit={handleSubmit} className="login-form">
          {/* Username Field */}
          <div className="form-field">
            <label htmlFor="username">Username</label>
            <div className="input-wrapper">
              <svg className="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd"/>
              </svg>
              <input
                id="username"
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Choose a username"
                required
                autoComplete="username"
              />
            </div>
          </div>
          
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
                placeholder="your@email.com"
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
                placeholder="Create a strong password"
                required
                autoComplete="new-password"
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
            
            {/* Password Strength Indicator */}
            {formData.password && (
              <div className="password-strength">
                <div className="strength-indicators">
                  <div className={`strength-item ${passwordStrength.hasLength ? 'valid' : 'invalid'}`}>
                    {passwordStrength.hasLength ? '✓' : '○'} 8+ characters
                  </div>
                  <div className={`strength-item ${passwordStrength.hasUpper ? 'valid' : 'invalid'}`}>
                    {passwordStrength.hasUpper ? '✓' : '○'} 1 uppercase
                  </div>
                  <div className={`strength-item ${passwordStrength.hasSpecial ? 'valid' : 'invalid'}`}>
                    {passwordStrength.hasSpecial ? '✓' : '○'} 1 special char
                  </div>
                </div>
                <div className={`strength-message ${passwordStrength.isValid ? 'valid' : 'invalid'}`}>
                  {passwordStrength.message}
                </div>
              </div>
            )}
          </div>
          
          {/* Submit Button */}
          <button 
            type="submit" 
            disabled={loading || (formData.password && !passwordStrength.isValid)} 
            className="login-submit"
          >
            {loading ? (
              <>
                <span className="button-spinner"></span>
                Creating Account...
              </>
            ) : (
              'Create Account'
            )}
          </button>
        </form>
        
        {/* Login Link */}
        <div className="login-signup">
          Already have an account? <Link to="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}

export default Signup;