import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './Navbar';

function Dashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users/');
        setUsers(response.data);
        setLoading(false);
      } catch (err) {
        if (err.response?.status === 401) {
          setError('Session expired. Please log in again.');
        } else {
          setError('Failed to load users.');
        }
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <Navbar />

      <div style={{ padding: '30px', maxWidth: '1000px', margin: '0 auto' }}>
        <h1>Dashboard</h1>
        <p>Welcome! Here are all registered users:</p>

        {loading && <p>Loading users...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {!loading && !error && (
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '20px'
          }}>
            <thead>
              <tr style={{ background: '#f8f9fa' }}>
                <th style={{ padding: '12px', border: '1px solid #dee2e6', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '12px', border: '1px solid #dee2e6', textAlign: 'left' }}>Name</th>
                <th style={{ padding: '12px', border: '1px solid #dee2e6', textAlign: 'left' }}>Email</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr>
                  <td colSpan="3" style={{ padding: '20px', textAlign: 'center' }}>
                    No users found.
                  </td>
                </tr>
              ) : (
                users.map(user => (
                  <tr key={user.id}>
                    <td style={{ padding: '12px', border: '1px solid #dee2e6' }}>{user.id}</td>
                    <td style={{ padding: '12px', border: '1px solid #dee2e6' }}>{user.name}</td>
                    <td style={{ padding: '12px', border: '1px solid #dee2e6' }}>{user.email}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Dashboard;