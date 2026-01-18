import React, { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import api from '../utils/api';  // ✅ Use the api instance, not axios

function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!token) {
      setError('Invalid or missing reset token');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      // ✅ Use api instance instead of axios directly
      const response = await api.post('/api/reset-password', {
        token: token,
        password: password,
      });

      console.log('✅ Password reset successful:', response.data);
      setSuccess(true);

      // Redirect to login after 2 seconds
      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      console.error('❌ Reset error:', err.response?.data);
      setError(err.response?.data?.error || 'Reset failed. Link may be invalid or expired.');
    } finally {
      setLoading(false);
    }
  };

  // Success state
  if (success) {
    return (
      <div style={{ maxWidth: '400px', margin: '100px auto', textAlign: 'center' }}>
        <h2 style={{ color: 'green' }}>✅ Password Reset Successful!</h2>
        <p>Redirecting to login...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto' }}>
      <h2>Reset Password</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="New password (min 8 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />

        <input
          type="password"
          placeholder="Confirm password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          required
        />

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <button 
          type="submit" 
          disabled={loading || !password || !confirmPassword}
          style={{ width: '100%', padding: '10px' }}
        >
          {loading ? 'Resetting...' : 'Reset Password'}
        </button>
      </form>

      <div style={{ marginTop: '10px' }}>
        <a href="/login">Back to login</a>
      </div>
    </div>
  );
}

export default ResetPassword;