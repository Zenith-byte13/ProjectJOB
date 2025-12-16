import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if token exists in localStorage on app start
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // Set default header for all axios requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // Optionally: fetch user info or just mark as logged in
      // For now, we just assume valid token = logged in
      setCurrentUser({ isAuthenticated: true });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      const token = response.data.access_token;

      // Store token
      localStorage.setItem('access_token', token);

      // Set default Authorization header for future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      setCurrentUser({ isAuthenticated: true });
      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'Invalid credentials' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    delete axios.defaults.headers.common['Authorization'];
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    login,
    logout,
    loading
  };

  return (
  <AuthContext.Provider value={value}>
    {loading ? (
      <div style={{ 
        textAlign: 'center', 
        marginTop: '200px', 
        fontSize: '20px' 
      }}>
        Loading...
      </div>
    ) : (
      children
    )}
  </AuthContext.Provider>
  );
};