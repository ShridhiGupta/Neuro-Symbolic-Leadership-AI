import axios from 'axios';

// API service for Vercel deployment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

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

// API service methods for Vercel deployment
export const apiService = {
  // Assessment endpoints (using Vercel serverless functions)
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

  // Upload endpoints (using Vercel serverless functions)
  upload: {
    resume: (formData, userId) => {
      // For file uploads, we need to use a different approach with Vercel
      // This would require a file upload service like Vercel Blob or AWS S3
      console.warn('File upload not supported in Vercel serverless. Use text upload instead.');
      return Promise.resolve({
        filename: 'sample_resume.pdf',
        file_size: 1024000,
        extracted_text: 'Sample resume text for demonstration purposes.',
        text_length: 100,
        status: 'success',
        message: 'File upload simulated (use text upload for actual functionality)'
      });
    },
    text: (data) => api.post('/api/upload/text', data),
    getSupportedFormats: () => api.get('/api/upload/supported-formats'),
    deleteFile: (filename) => api.delete(`/api/upload/${filename}`),
    listFiles: () => api.get('/api/upload/'),
  },

  // Analysis endpoints (using Vercel serverless functions)
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
