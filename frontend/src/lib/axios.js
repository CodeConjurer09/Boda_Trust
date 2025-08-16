import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' }
});

// Attach token from localStorage before every request
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Optional: handle expired token globally
instance.interceptors.response.use(
  res => res,
  err => {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem('access');
      // Optionally redirect to login page:
      // window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default instance;
