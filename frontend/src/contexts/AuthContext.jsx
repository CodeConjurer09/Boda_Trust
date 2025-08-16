import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from '../lib/axios';

const AuthContext = createContext();
export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access') || null);
  const [loading, setLoading] = useState(true);

  // Attach token to all requests automatically (optional improvement)
  useEffect(() => {
    const interceptor = axios.interceptors.request.use((config) => {
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      return config;
    });
    return () => axios.interceptors.request.eject(interceptor);
  }, [accessToken]);

  useEffect(() => {
    async function fetchUser() {
      if (!accessToken) {
        setUser(null);
        setLoading(false);
        return;
      }
      try {
        const res = await axios.get('/accounts/me/');
        setUser(res.data);
      } catch (err) {
        console.error('Failed to fetch user profile', err);
        setUser(null);
        setAccessToken(null);
        localStorage.removeItem('access');
      } finally {
        setLoading(false);
      }
    }
    fetchUser();
  }, [accessToken]);

  const login = async (email, password) => {
    try {
      const res = await axios.post('/accounts/login/', { email, password });
      const token = res.data.access;
      setAccessToken(token);
      localStorage.setItem('access', token);
      const profile = await axios.get('/accounts/me/');
      setUser(profile.data);
    } catch (err) {
      console.error('Login failed', err);
      throw err; // Let the calling component show an error message
    }
  };

  const logout = () => {
    setUser(null);
    setAccessToken(null);
    localStorage.removeItem('access');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, accessToken, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
