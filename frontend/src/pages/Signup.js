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
        <h1>Medical Report Summarizer</h1>
        <h2>Sign Up</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Choose a username"
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your@email.com"
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
              placeholder="Min 8 chars, 1 uppercase, 1 special"
            />
            
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
          
          <button 
            type="submit" 
            disabled={loading || (formData.password && !passwordStrength.isValid)} 
            className="btn-primary"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
        
        <p className="auth-link">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;