import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; // Assuming you have a CSS file for styling

const Home: React.FC = () => {
    return (
        <div className="home-container">
            <header className="home-header">
                <h1>Welcome to ElevateU</h1>
                <p>Showcase your achievements and inspire your campus community!</p>
                <nav>
                    <Link to="/login">Login</Link>
                    <Link to="/signup">Signup</Link>
                </nav>
            </header>
            <main className="home-content">
                <section className="achievements-section">
                    <h2>Recent Achievements</h2>
                    {/* Placeholder for achievements list */}
                </section>
                <section className="leaderboard-section">
                    <h2>Leaderboard</h2>
                    {/* Placeholder for leaderboard */}
                </section>
            </main>
        </div>
    );
};

export default Home;