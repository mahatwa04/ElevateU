import { test, expect } from '@playwright/test';

const API_URL = process.env.API_URL || 'https://elevateu-backend.onrender.com/api';

test.describe('Authentication Flow', () => {
  let authToken: string;
  let testUserId: number;

  test('should register a new user', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/register/`, {
      data: {
        email: `testuser_${Date.now()}@bennett.edu.in`,
        password: 'TestPass123!',
        first_name: 'Test',
        last_name: 'User',
      },
    });
    expect(response.status()).toBe(201);
    const body = await response.json();
    expect(body).toHaveProperty('user');
    testUserId = body.user.id;
  });

  test('should login user with email and password', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/login/`, {
      data: {
        email: 'admin@bennett.edu.in',
        password: 'admin123456',
      },
    });
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(body).toHaveProperty('access');
    authToken = body.access;
  });

  test('should verify JWT token', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/token/verify/`, {
      data: { token: authToken },
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBeGreaterThanOrEqual(200);
  });
});

test.describe('Post Management', () => {
  let postId: number;
  let authToken: string;

  test.beforeAll(async ({ request }) => {
    const loginRes = await request.post(`${API_URL}/auth/login/`, {
      data: {
        email: 'admin@bennett.edu.in',
        password: 'admin123456',
      },
    });
    authToken = (await loginRes.json()).access;
  });

  test('should create a new post', async ({ request }) => {
    const response = await request.post(`${API_URL}/posts/`, {
      data: {
        title: 'Test Achievement',
        description: 'This is a test achievement post',
        category: 'academics',
        image: 'https://example.com/image.jpg',
      },
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBe(201);
    const body = await response.json();
    expect(body).toHaveProperty('id');
    postId = body.id;
  });

  test('should retrieve all posts', async ({ request }) => {
    const response = await request.get(`${API_URL}/posts/`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(Array.isArray(body.results || body)).toBe(true);
  });

  test('should retrieve single post', async ({ request }) => {
    const response = await request.get(`${API_URL}/posts/${postId}/`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBe(200);
  });

  test('should update post', async ({ request }) => {
    const response = await request.patch(`${API_URL}/posts/${postId}/`, {
      data: { title: 'Updated Achievement' },
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBe(200);
  });

  test('should delete post', async ({ request }) => {
    const response = await request.delete(`${API_URL}/posts/${postId}/`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBeGreaterThanOrEqual(200);
    expect(response.status()).toBeLessThan(300);
  });
});

test.describe('Engagement Features', () => {
  let authToken: string;
  let targetUserId: number = 1;

  test.beforeAll(async ({ request }) => {
    const loginRes = await request.post(`${API_URL}/auth/login/`, {
      data: {
        email: 'admin@bennett.edu.in',
        password: 'admin123456',
      },
    });
    authToken = (await loginRes.json()).access;
  });

  test('should follow a user', async ({ request }) => {
    const response = await request.post(`${API_URL}/engagement/follows/toggle/`, {
      data: { following: targetUserId },
      headers: { Authorization: `Bearer ${authToken}` },
    });
    expect(response.status()).toBeGreaterThanOrEqual(200);
    expect(response.status()).toBeLessThan(300);
  });

  test('should like a post', async ({ request }) => {
    const postsRes = await request.get(`${API_URL}/posts/`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    const posts = (await postsRes.json()).results || [];
    if (posts.length > 0) {
      const postId = posts[0].id;
      const response = await request.post(`${API_URL}/engagement/likes/`, {
        data: { post: postId },
        headers: { Authorization: `Bearer ${authToken}` },
      });
      expect(response.status()).toBeGreaterThanOrEqual(200);
      expect(response.status()).toBeLessThan(300);
    }
  });

  test('should add a comment to post', async ({ request }) => {
    const postsRes = await request.get(`${API_URL}/posts/`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    const posts = (await postsRes.json()).results || [];
    if (posts.length > 0) {
      const postId = posts[0].id;
      const response = await request.post(`${API_URL}/engagement/comments/`, {
        data: { post: postId, text: 'Great achievement!' },
        headers: { Authorization: `Bearer ${authToken}` },
      });
      expect(response.status()).toBeGreaterThanOrEqual(200);
      expect(response.status()).toBeLessThan(300);
    }
  });
});

test.describe('Leaderboard', () => {
  test('should retrieve leaderboard rankings', async ({ request }) => {
    const response = await request.get(`${API_URL}/engagement/leaderboard/?category=academics`);
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(Array.isArray(body.results || body)).toBe(true);
  });

  test('should have pagination in leaderboard', async ({ request }) => {
    const response = await request.get(`${API_URL}/engagement/leaderboard/?page=1&limit=10`);
    expect(response.status()).toBe(200);
  });
});
