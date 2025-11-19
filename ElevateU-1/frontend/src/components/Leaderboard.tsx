import React, { useEffect, useState } from 'react';
import { getLeaderboard } from '../services/api';

const Leaderboard: React.FC = () => {
    const [rankings, setRankings] = useState([]);

    useEffect(() => {
        const fetchRankings = async () => {
            const data = await getLeaderboard();
            setRankings(data);
        };

        fetchRankings();
    }, []);

    return (
        <div className="leaderboard">
            <h2>Leaderboard</h2>
            <ul>
                {rankings.map((user, index) => (
                    <li key={user.id}>
                        <span>{index + 1}. {user.name} - {user.score} points</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Leaderboard;