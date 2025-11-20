import React from 'react';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../services/api';

const Profile = () => {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [achievements, setAchievements] = useState([]);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const response = await api.get(`/users/${userId}`);
                setUser(response.data);
                const achievementsResponse = await api.get(`/posts?userId=${userId}`);
                setAchievements(achievementsResponse.data);
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };

        fetchUserProfile();
    }, [userId]);

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div className="profile">
            <h1>{user.username}'s Profile</h1>
            <p>Email: {user.email}</p>
            <h2>Achievements</h2>
            <ul>
                {achievements.map((achievement) => (
                    <li key={achievement.id}>
                        <h3>{achievement.title}</h3>
                        <p>{achievement.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Profile;