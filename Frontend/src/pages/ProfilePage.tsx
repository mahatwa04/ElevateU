import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { userAPI, engagementAPI, User } from '../services/api';
import '../styles/ProfilePage.css';

const ProfilePage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [user, setUser] = useState<User | null>(null);
  const [followers, setFollowers] = useState<User[]>([]);
  const [following, setFollowing] = useState<User[]>([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const currentUserId = localStorage.getItem('user_id');
  const isOwnProfile = currentUserId === userId;

  useEffect(() => {
    fetchUserData();
  }, [userId]);

  const fetchUserData = async () => {
    if (!userId) return;

    try {
      setLoading(true);
      const userResponse = await userAPI.getUserDetails(parseInt(userId));
      setUser(userResponse.data);

      const followersResponse = await userAPI.getFollowers(parseInt(userId));
      setFollowers(followersResponse.data || []);

      const followingResponse = await userAPI.getFollowing(parseInt(userId));
      setFollowing(followingResponse.data || []);
    } catch (err: any) {
      setError('Failed to load profile');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFollowUnfollow = async () => {
    if (!userId) return;

    try {
      if (isFollowing) {
        await engagementAPI.unfollowUser(parseInt(userId));
      } else {
        await engagementAPI.followUser(parseInt(userId));
      }
      setIsFollowing(!isFollowing);
      fetchUserData();
    } catch (err: any) {
      setError('Failed to update follow status');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="profile-page">
        <div className="loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="profile-page">
        <div className="container">
          <div className="error">{error || 'User not found'}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="container">
          <div className="profile-info">
            <div className="profile-avatar">
              {user.profile_picture ? (
                <img src={user.profile_picture} alt={user.username} />
              ) : (
                <div className="avatar-placeholder">{user.username.charAt(0).toUpperCase()}</div>
              )}
            </div>

            <div className="profile-details">
              <h1>{user.first_name} {user.last_name}</h1>
              <p className="username">@{user.username}</p>
              <p className="field">{user.field}</p>
              {user.bio && <p className="bio">{user.bio}</p>}

              {!isOwnProfile && (
                <button
                  className={`btn ${isFollowing ? 'btn-outline' : 'btn-primary'}`}
                  onClick={handleFollowUnfollow}
                >
                  {isFollowing ? 'Unfollow' : 'Follow'}
                </button>
              )}
            </div>

            <div className="profile-stats">
              <div className="stat">
                <div className="stat-value">{followers.length}</div>
                <div className="stat-label">Followers</div>
              </div>
              <div className="stat">
                <div className="stat-value">{following.length}</div>
                <div className="stat-label">Following</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="profile-content">
        <div className="container">
          <div className="profile-section">
            <h2>Followers ({followers.length})</h2>
            {followers.length === 0 ? (
              <p className="empty">No followers yet</p>
            ) : (
              <div className="user-list">
                {followers.map((follower) => (
                  <div key={follower.id} className="user-card">
                    <div className="user-info">
                      <h4>{follower.first_name} {follower.last_name}</h4>
                      <p>@{follower.username}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="profile-section">
            <h2>Following ({following.length})</h2>
            {following.length === 0 ? (
              <p className="empty">Not following anyone yet</p>
            ) : (
              <div className="user-list">
                {following.map((followingUser) => (
                  <div key={followingUser.id} className="user-card">
                    <div className="user-info">
                      <h4>{followingUser.first_name} {followingUser.last_name}</h4>
                      <p>@{followingUser.username}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
