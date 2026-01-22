import axios from 'axios';

const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://medical-backend-wbqv.onrender.com'
    : 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If 401 Unauthorized, redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

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
  
  // 🔥 NEW: Compare two reports
  compareReports: (formData) =>
    api.post('/api/report/compare', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  
  // 🔥 NEW: Calculate health risks
  calculateRisks: (reportId) => api.get(`/api/report/calculate-risks/${reportId}`),
};

// JARGON API
export const jargonAPI = {
  explain: (term) => api.post('/api/jargon/explain', { term }),
};

export default api;