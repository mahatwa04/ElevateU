import React, { useState, useEffect } from 'react';
import { leaderboardAPI, Leaderboard } from '../services/api';
import '../styles/LeaderboardPage.css';

const LeaderboardPage: React.FC = () => {
  const [leaderboards, setLeaderboards] = useState<Leaderboard[]>([]);
  const [selectedField, setSelectedField] = useState('academics');
  const [selectedPeriod, setSelectedPeriod] = useState('ALL_TIME');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fields = ['academics', 'sports', 'music', 'dance', 'leadership'];
  const periods = [
    { value: 'ALL_TIME', label: 'All Time' },
    { value: 'MONTHLY', label: 'This Month' },
    { value: 'WEEKLY', label: 'This Week' },
  ];

  useEffect(() => {
    fetchLeaderboard();
  }, [selectedField, selectedPeriod]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await leaderboardAPI.getLeaderboard(selectedField, selectedPeriod);
      setLeaderboards(response.data || []);
    } catch (err: any) {
      setError('Failed to load leaderboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="leaderboard-page">
      <div className="container">
        <div className="leaderboard-header">
          <h1>🏆 Leaderboard</h1>
          <p>Top achievers on campus</p>
        </div>

        <div className="leaderboard-filters">
          <div className="filter-group">
            <label>Field</label>
            <div className="filter-buttons">
              {fields.map((field) => (
                <button
                  key={field}
                  className={`filter-btn ${selectedField === field ? 'active' : ''}`}
                  onClick={() => setSelectedField(field)}
                >
                  {field.charAt(0).toUpperCase() + field.slice(1)}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-group">
            <label>Time Period</label>
            <div className="filter-buttons">
              {periods.map((period) => (
                <button
                  key={period.value}
                  className={`filter-btn ${selectedPeriod === period.value ? 'active' : ''}`}
                  onClick={() => setSelectedPeriod(period.value)}
                >
                  {period.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
          </div>
        ) : leaderboards.length === 0 ? (
          <div className="empty-state">
            <p>No data available for this field and period</p>
          </div>
        ) : (
          <div className="leaderboard-table">
            <div className="table-header">
              <div className="rank">Rank</div>
              <div className="name">User</div>
              <div className="points">Points</div>
              <div className="achievements">Achievements</div>
            </div>

            {leaderboards.map((entry, index) => (
              <div key={entry.user.id} className="table-row">
                <div className="rank">
                  <span className={`rank-badge rank-${index + 1 <= 3 ? index + 1 : 'other'}`}>
                    {entry.rank || index + 1}
                  </span>
                </div>
                <div className="name">
                  <div className="user-avatar">
                    {entry.user.profile_picture ? (
                      <img src={entry.user.profile_picture} alt={entry.user.username} />
                    ) : (
                      <div>{entry.user.username.charAt(0).toUpperCase()}</div>
                    )}
                  </div>
                  <div className="user-details">
                    <p className="username">{entry.user.first_name} {entry.user.last_name}</p>
                    <p className="field-tag">{entry.user.field}</p>
                  </div>
                </div>
                <div className="points">
                  <strong>{entry.points || 0}</strong>
                  <span>pts</span>
                </div>
                <div className="achievements">
                  {entry.achievements_count || 0}
                  <span> achievements</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LeaderboardPage;
