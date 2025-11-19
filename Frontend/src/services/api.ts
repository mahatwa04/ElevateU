import axios, { AxiosInstance, AxiosError } from 'axios';

// Configure API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest: any = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_id');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// ============================================================================
// AUTH ENDPOINTS (4)
// ============================================================================

export const authAPI = {
  // Register new user
  register: (userData: {
    username: string;
    email: string;
    password: string;
    password2: string;
    first_name?: string;
    last_name?: string;
    field?: string;
  }) => api.post('/auth/register/', userData),

  // Verify email with OTP
  verifyEmail: (email: string, otp: string) =>
    api.post('/auth/verify-email/', { email, otp }),

  // Login user
  login: (email: string, password: string) =>
    api.post('/auth/login/', { email, password }),

  // Refresh JWT token
  refreshToken: (refreshToken: string) =>
    api.post('/token/refresh/', { refresh: refreshToken }),
};

// ============================================================================
// USER MANAGEMENT ENDPOINTS (5)
// ============================================================================

export const userAPI = {
  // Get current user profile
  getCurrentProfile: () => api.get('/users/profile/'),

  // Get user details by ID
  getUserDetails: (userId: number) => api.get(`/users/${userId}/`),

  // Update user profile
  updateProfile: (userId: number, userData: any) =>
    api.put(`/users/${userId}/`, userData),

  // Get user followers
  getFollowers: (userId: number) => api.get(`/users/${userId}/followers/`),

  // Get user following
  getFollowing: (userId: number) => api.get(`/users/${userId}/following/`),
};

// ============================================================================
// POST ENDPOINTS (5)
// ============================================================================

export const postAPI = {
  // Create new post
  createPost: (postData: {
    title: string;
    description: string;
    category?: string;
    image?: string;
  }) => api.post('/posts/', postData),

  // List all posts with pagination
  listPosts: (page: number = 1, pageSize: number = 10) =>
    api.get('/posts/', { params: { page, page_size: pageSize } }),

  // Get post details
  getPost: (postId: number) => api.get(`/posts/${postId}/`),

  // Update post
  updatePost: (postId: number, postData: any) =>
    api.put(`/posts/${postId}/`, postData),

  // Delete post
  deletePost: (postId: number) => api.delete(`/posts/${postId}/`),
};

// ============================================================================
// ENGAGEMENT ENDPOINTS (10)
// ============================================================================

export const engagementAPI = {
  // Like a post
  likePost: (postId: number) => api.post(`/posts/${postId}/like/`),

  // Unlike a post
  unlikePost: (postId: number) => api.delete(`/posts/${postId}/like/`),

  // Add comment to post
  addComment: (postId: number, commentData: { text: string }) =>
    api.post(`/posts/${postId}/comments/`, commentData),

  // Get post comments
  getComments: (postId: number, page: number = 1, pageSize: number = 10) =>
    api.get(`/posts/${postId}/comments/`, {
      params: { page, page_size: pageSize },
    }),

  // Update comment
  updateComment: (commentId: number, commentData: { text: string }) =>
    api.put(`/comments/${commentId}/`, commentData),

  // Delete comment
  deleteComment: (commentId: number) => api.delete(`/comments/${commentId}/`),

  // Follow a user
  followUser: (userId: number) => api.post(`/users/${userId}/follow/`),

  // Unfollow a user
  unfollowUser: (userId: number) => api.delete(`/users/${userId}/follow/`),

  // Get engagement (likes, comments, follows)
  getEngagement: () => api.get('/engagement/'),

  // Get user endorsements
  getUserEndorsements: (userId: number) =>
    api.get(`/users/${userId}/endorsements/`),
};

// ============================================================================
// LEADERBOARD ENDPOINTS (4)
// ============================================================================

export const leaderboardAPI = {
  // Get leaderboard by field and time period
  getLeaderboard: (field: string = 'academics', timePeriod: string = 'ALL_TIME') =>
    api.get('/leaderboard/', { params: { field, time_period: timePeriod } }),

  // Get user rankings
  getUserRankings: (userId: number) =>
    api.get(`/leaderboard/user/${userId}/`),

  // Calculate rankings
  calculateRankings: () => api.post('/rankings/calculate/'),

  // Create endorsement
  createEndorsement: (userId: number, endorsementData: { skill: string }) =>
    api.post(`/users/${userId}/endorsements/`, endorsementData),
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

export const tokenAPI = {
  // Store tokens
  setTokens: (accessToken: string, refreshToken: string) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  },

  // Get access token
  getAccessToken: () => localStorage.getItem('access_token'),

  // Get refresh token
  getRefreshToken: () => localStorage.getItem('refresh_token'),

  // Clear tokens (logout)
  clearTokens: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
  },

  // Check if user is authenticated
  isAuthenticated: () => !!localStorage.getItem('access_token'),
};

// ============================================================================
// TYPES
// ============================================================================

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  field: string;
  bio?: string;
  profile_picture?: string;
  created_at: string;
}

export interface Post {
  id: number;
  title: string;
  description: string;
  category: string;
  image?: string;
  user: User;
  like_count: number;
  comment_count: number;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: number;
  text: string;
  user: User;
  post: number;
  created_at: string;
}

export interface Like {
  id: number;
  user: User;
  post: number;
  created_at: string;
}

export interface Follow {
  id: number;
  follower: User;
  following: User;
  created_at: string;
}

export interface Leaderboard {
  user: User;
  rank: number;
  points: number;
  achievements_count: number;
}

export interface Endorsement {
  id: number;
  skill: string;
  endorsed_by: User;
  created_at: string;
}

export interface ApiError {
  message: string;
  error: any;
}

export default api;
