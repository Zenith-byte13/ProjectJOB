import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav style={{
      background: '#343a40',
      padding: '15px',
      color: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '20px' }}>
        UserApp
      </Link>

      <div>
        {currentUser ? (
          <>
            <Link to="/dashboard" style={{ color: 'white', marginRight: '20px', textDecoration: 'none' }}>
              Dashboard
            </Link>
            <button
              onClick={handleLogout}
              style={{
                background: '#dc3545',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ color: 'white', marginRight: '15px', textDecoration: 'none' }}>
              Login
            </Link>
            <Link to="/signup" style={{ color: 'white', textDecoration: 'none' }}>
              Signup
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;