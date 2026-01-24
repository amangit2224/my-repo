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
  timeout: 120000, // 2 minutes timeout for large uploads
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

// Enhanced error message formatter
const getErrorMessage = (error) => {
  // Network errors (no response from server)
  if (!error.response) {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      return {
        title: '⏰ Request Timeout',
        message: 'The operation took too long. Please try again with a smaller file or check your internet connection.',
        type: 'timeout'
      };
    }
    if (error.message === 'Network Error' || !navigator.onLine) {
      return {
        title: '🌐 Connection Lost',
        message: 'Unable to reach the server. Please check your internet connection and try again.',
        type: 'network'
      };
    }
    return {
      title: '❌ Connection Error',
      message: 'Unable to connect to the server. Please check your internet connection.',
      type: 'network'
    };
  }

  const status = error.response.status;
  const data = error.response.data;

  // Status-based error messages
  switch (status) {
    case 400:
      return {
        title: '⚠️ Invalid Request',
        message: data.error || data.message || 'Please check your input and try again.',
        type: 'validation'
      };
    
    case 401:
      return {
        title: '🔒 Session Expired',
        message: 'Your session has expired. Please login again.',
        type: 'auth'
      };
    
    case 403:
      return {
        title: '🚫 Access Denied',
        message: 'You don\'t have permission to perform this action.',
        type: 'permission'
      };
    
    case 404:
      return {
        title: '🔍 Not Found',
        message: data.error || 'The requested resource was not found.',
        type: 'notfound'
      };
    
    case 413:
      return {
        title: '📦 File Too Large',
        message: 'The file you\'re trying to upload is too large. Please compress it and try again.',
        type: 'filesize'
      };
    
    case 429:
      return {
        title: '⏰ Rate Limit Reached',
        message: 'You\'ve reached the daily upload limit. Please try again tomorrow or upgrade your plan.',
        type: 'ratelimit'
      };
    
    case 500:
      return {
        title: '🔧 Server Error',
        message: 'Something went wrong on our end. Our team has been notified. Please try again later.',
        type: 'server'
      };
    
    case 502:
    case 503:
    case 504:
      return {
        title: '⚠️ Service Unavailable',
        message: 'The server is temporarily unavailable. Please try again in a few moments.',
        type: 'unavailable'
      };
    
    default:
      return {
        title: '❌ Error',
        message: data.error || data.message || 'An unexpected error occurred. Please try again.',
        type: 'unknown'
      };
  }
};

// Response interceptor - enhanced error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Get formatted error message
    const errorInfo = getErrorMessage(error);
    
    // Attach formatted error to the error object
    error.userMessage = errorInfo.message;
    error.userTitle = errorInfo.title;
    error.errorType = errorInfo.type;
    
    // If 401 Unauthorized, redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      
      // Only redirect if not already on login/signup page
      if (!window.location.pathname.includes('/login') && 
          !window.location.pathname.includes('/signup')) {
        window.location.href = '/login';
      }
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
      timeout: 180000, // 3 minutes for uploads
    }),
  getHistory: () => api.get('/api/report/history'),
  getDetails: (reportId) => api.get(`/api/report/details/${reportId}`),
  
  // Compare two reports
  compareReports: (formData) =>
    api.post('/api/report/compare', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 180000,
    }),
  
  // Calculate health risks
  calculateRisks: (reportId) => api.get(`/api/report/calculate-risks/${reportId}`),
  
  // Get diet recommendations
  getDietRecommendations: (reportId) => api.get(`/api/report/diet-recommendations/${reportId}`),
  
  // Chat with report
  chatWithReport: (reportId, data) => api.post(`/api/report/chat/${reportId}`, data),
  
  // Get chat suggestions
  getChatSuggestions: (reportId) => api.get(`/api/report/chat/suggestions/${reportId}`),
};

// JARGON API
export const jargonAPI = {
  explain: (term) => api.post('/api/jargon/explain', { term }),
};

// Helper function to get user-friendly error message from API error
export const getApiErrorMessage = (error) => {
  return error.userMessage || error.response?.data?.error || error.message || 'An unexpected error occurred';
};

// Helper function to check if error is specific type
export const isErrorType = (error, type) => {
  return error.errorType === type;
};

export default api;