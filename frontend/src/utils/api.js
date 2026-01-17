import axios from 'axios';

// Use this structure as specified
const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://medical-backend-wbqv.onrender.com'
    : 'http://localhost:5000';

// Remove the old API_BASE_URL and use the new one above
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// AUTH API
export const authAPI = {
  signup: (data) => api.post('/api/auth/signup', data),
  login: (data) => api.post('/api/auth/login', data),
};

// REPORT API
export const reportAPI = {
  upload: (formData) =>
    api.post('/api/report/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getHistory: () => api.get('/api/report/history'),
  getDetails: (reportId) => api.get(`/api/report/details/${reportId}`),
};

export const jargonAPI = {
  explain: (term) => api.post('/api/jargon/explain', { term }),
};

export default api;