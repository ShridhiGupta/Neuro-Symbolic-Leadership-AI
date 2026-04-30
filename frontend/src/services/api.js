import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
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

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API service methods
export const apiService = {
  // Assessment endpoints
  assessment: {
    evaluate: (data) => api.post('/api/assessment/evaluate', data),
    analyzeText: (data) => api.post('/api/assessment/analyze-text', data),
    getCulturalComparison: (userId, text) => 
      api.get(`/api/assessment/cultural-comparison/${userId}`, { params: { text } }),
    getTraitDevelopment: (traitName, currentScore) =>
      api.get(`/api/assessment/trait-development/${traitName}`, { params: { current_score: currentScore } }),
    getUserAssessments: (userId) => api.get(`/api/assessment/user-assessments/${userId}`),
    compareAssessments: (userId, assessmentIds) =>
      api.post('/api/assessment/compare-assessments', { user_id: userId, assessment_ids: assessmentIds }),
    getSupportedCultures: () => api.get('/api/assessment/supported-cultures'),
    getLeadershipTraits: () => api.get('/api/assessment/leadership-traits'),
  },

  // Upload endpoints
  upload: {
    resume: (formData, userId) => api.post('/api/upload/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      params: { user_id: userId },
    }),
    text: (data) => api.post('/api/upload/text', data),
    getSupportedFormats: () => api.get('/api/upload/supported-formats'),
    deleteFile: (filename) => api.delete(`/api/upload/${filename}`),
    listFiles: () => api.get('/api/upload/'),
  },

  // Analysis endpoints
  analysis: {
    communicationStyle: (text) => api.post('/api/analysis/communication-style', { text }),
    leadershipTraits: (text) => api.post('/api/analysis/leadership-traits', { text }),
    resumeExtraction: (text) => api.post('/api/analysis/resume-extraction', { text }),
    textFeatures: (text) => api.post('/api/analysis/text-features', { text }),
  },

  // Health check
  health: () => api.get('/health'),
};

// Export the default api instance for direct use
export default api;
