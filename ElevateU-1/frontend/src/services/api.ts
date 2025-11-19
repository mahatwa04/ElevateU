import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Adjust the base URL as needed

// Function to handle user signup
export const signup = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/users/signup/`, userData);
    return response.data;
};

// Function to handle user login
export const login = async (credentials) => {
    const response = await axios.post(`${API_BASE_URL}/users/login/`, credentials);
    return response.data;
};

// Function to post an achievement
export const postAchievement = async (achievementData) => {
    const response = await axios.post(`${API_BASE_URL}/posts/`, achievementData);
    return response.data;
};

// Function to like a post
export const likePost = async (postId) => {
    const response = await axios.post(`${API_BASE_URL}/posts/${postId}/like/`);
    return response.data;
};

// Function to comment on a post
export const commentOnPost = async (postId, commentData) => {
    const response = await axios.post(`${API_BASE_URL}/posts/${postId}/comments/`, commentData);
    return response.data;
};

// Function to get the leaderboard
export const getLeaderboard = async () => {
    const response = await axios.get(`${API_BASE_URL}/leaderboard/`);
    return response.data;
};

// Function to follow a user
export const followUser = async (userId) => {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/follow/`);
    return response.data;
};