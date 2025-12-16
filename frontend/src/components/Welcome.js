import { Link } from 'react-router-dom';

function Welcome() {
  return (
    <div style={{
      textAlign: 'center',
      marginTop: '100px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1>Welcome to User Management App</h1>
      <p style={{ fontSize: '18px', margin: '30px 0' }}>
        Manage users with a secure and modern interface.
      </p>

      <div style={{ margin: '30px 0' }}>
        <Link
          to="/login"
          style={{
            margin: '0 15px',
            padding: '12px 30px',
            background: '#007bff',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '5px'
          }}
        >
          Login
        </Link>

        <Link
          to="/signup"
          style={{
            margin: '0 15px',
            padding: '12px 30px',
            background: '#28a745',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '5px'
          }}
        >
          Signup
        </Link>
      </div>

      <p>
        <Link to="/forgot-password">Forgot Password?</Link>
      </p>
    </div>
  );
}

export default Welcome;