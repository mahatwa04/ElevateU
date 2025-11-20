import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { tokenAPI, userAPI } from '../services/api';
import '../styles/Navbar.css';

interface NavbarProps {
  onLogout: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onLogout }) => {
  const navigate = useNavigate();
  const [userName, setUserName] = React.useState('');

  React.useEffect(() => {
    // Fetch current user profile
    userAPI
      .getCurrentProfile()
      .then((response) => {
        setUserName(response.data.username);
      })
      .catch((error) => {
        console.error('Failed to fetch user profile:', error);
      });
  }, []);

  const handleLogout = () => {
    tokenAPI.clearTokens();
    onLogout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🎯</span>
          <span className="brand-text">ElevateU</span>
        </Link>

        <div className="navbar-menu">
          <Link to="/" className="nav-link">
            Feed
          </Link>
          <Link to="/leaderboard" className="nav-link">
            Leaderboard
          </Link>
          <Link to={`/profile/${localStorage.getItem('user_id') || ''}`} className="nav-link">
            Profile
          </Link>
        </div>

        <div className="navbar-right">
          <span className="username">Welcome, {userName}</span>
          <button className="btn btn-danger btn-small" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
