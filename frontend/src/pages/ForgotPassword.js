import React, { useState } from 'react';
import axios from 'axios';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await axios.post(
        'http://localhost:5000/api/forgot-password',
        { email: email.trim().toLowerCase() }
      );

      setMessage(response.data.message);
      setEmail('');
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto' }}>
      <h2>Forgot Password</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {message && <p style={{ color: 'green' }}>{message}</p>}

        <button
          type="submit"
          disabled={loading}
          style={{ width: '100%', padding: '10px' }}
        >
          {loading ? 'Sending...' : 'Send Reset Link'}
        </button>
      </form>

      <div style={{ marginTop: '10px' }}>
        <a href="/login">Back to login</a>
      </div>
    </div>
  );
}

export default ForgotPassword;
