# ElevateU Backend API Documentation

## Base URL
```
http://localhost:8000/api
```

---

## Authentication Endpoints

### 1. Register User
**Endpoint:** `POST /auth/register/`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@bennett.edu.in",
  "password": "securepassword123",
  "password2": "securepassword123",
  "field_of_interest": "academics",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@bennett.edu.in",
    "first_name": "John",
    "last_name": "Doe",
    "field_of_interest": "academics",
    "bio": null,
    "campus_verified": false
  },
  "message": "OTP sent to your campus email for verification."
}
```

---

### 2. Verify Email with OTP
**Endpoint:** `POST /auth/verify-email/`

**Request Body:**
```json
{
  "email": "john@bennett.edu.in",
  "otp_code": "123456"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@bennett.edu.in",
    "campus_verified": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Email verified successfully!"
}
```

---

### 3. Login (Get JWT Tokens)
**Endpoint:** `POST /auth/token/`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 4. Refresh Access Token
**Endpoint:** `POST /auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "new_access_token_here"
}
```

---

## User Endpoints

### 5. Get Current User Profile
**Endpoint:** `GET /users/profile/`
**Headers:** `Authorization: Bearer {access_token}`

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@bennett.edu.in",
  "first_name": "John",
  "last_name": "Doe",
  "field_of_interest": "academics",
  "bio": "Love coding!",
  "campus_verified": true
}
```

---

### 6. Update User Profile
**Endpoint:** `PUT /users/profile/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "bio": "Updated bio",
  "field_of_interest": "tech"
}
```

**Response (200 OK):** Updated user object

---

### 7. Get User Details
**Endpoint:** `GET /users/{user_id}/`

**Response (200 OK):** User object

---

### 8. Get User Followers
**Endpoint:** `GET /users/{user_id}/followers/`

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "username": "jane_doe",
    "email": "jane@bennett.edu.in"
  }
]
```

---

### 9. Get User Following
**Endpoint:** `GET /users/{user_id}/following/`

**Response (200 OK):** List of users

---

## Posts Endpoints

### 10. Create Post
**Endpoint:** `POST /posts/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "title": "Got A* in Database!",
  "description": "Studied hard for 3 months. Finally got the grade!",
  "category": "academics",
  "image": "https://example.com/image.jpg"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": "john_doe",
  "title": "Got A* in Database!",
  "description": "Studied hard for 3 months. Finally got the grade!",
  "category": "academics",
  "image": "https://example.com/image.jpg",
  "created_at": "2025-01-20T10:30:00Z",
  "updated_at": "2025-01-20T10:30:00Z",
  "like_count": 0,
  "comment_count": 0,
  "is_liked_by_user": false
}
```

---

### 11. Get All Posts
**Endpoint:** `GET /posts/`

**Query Parameters:**
- `search`: Search in title/description
- `category`: Filter by category
- `ordering`: Order by `created_at` or `like_count`

**Response (200 OK):** List of posts

---

### 12. Get Post Details
**Endpoint:** `GET /posts/{post_id}/`

**Response (200 OK):** Post object with comments and likes

---

### 13. Update Post
**Endpoint:** `PUT /posts/{post_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:** Same as create

**Response (200 OK):** Updated post

---

### 14. Delete Post
**Endpoint:** `DELETE /posts/{post_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Response (204 No Content)**

---

## Engagement Endpoints

### 15. Like a Post
**Endpoint:** `POST /engagement/likes/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "post": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": "john_doe",
  "post": 1,
  "created_at": "2025-01-20T10:35:00Z"
}
```

---

### 16. Unlike a Post
**Endpoint:** `DELETE /engagement/likes/{like_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Response (204 No Content)**

---

### 17. Add Comment
**Endpoint:** `POST /engagement/comments/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "post": 1,
  "text": "Congrats! Amazing achievement!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": "jane_doe",
  "post": 1,
  "text": "Congrats! Amazing achievement!",
  "created_at": "2025-01-20T10:40:00Z"
}
```

---

### 18. Get Post Comments
**Endpoint:** `GET /engagement/comments/?post_id={post_id}`

**Response (200 OK):** List of comments

---

### 19. Update Comment
**Endpoint:** `PUT /engagement/comments/{comment_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "text": "Updated comment text"
}
```

**Response (200 OK):** Updated comment

---

### 20. Delete Comment
**Endpoint:** `DELETE /engagement/comments/{comment_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Response (204 No Content)**

---

### 21. Follow a User
**Endpoint:** `POST /engagement/follow/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "following": 2
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "follower": "john_doe",
  "following": "jane_doe",
  "created_at": "2025-01-20T10:45:00Z"
}
```

---

### 22. Unfollow a User
**Endpoint:** `DELETE /engagement/unfollow/{user_id}/`
**Headers:** `Authorization: Bearer {access_token}`

**Response (200 OK):**
```json
{
  "message": "Unfollowed successfully"
}
```

---

### 23. Get Follow List
**Endpoint:** `GET /engagement/follows/`

**Response (200 OK):** List of all follows

---

## Leaderboard & Rankings Endpoints

### 24. Get Leaderboard
**Endpoint:** `GET /leaderboard/?field={field}&period={period}&limit={limit}`

**Query Parameters:**
- `field`: academics, sports, music, dance, tech, arts (default: academics)
- `period`: weekly, monthly, all_time (default: all_time)
- `limit`: Max results (default: 100)

**Response (200 OK):**
```json
[
  {
    "rank": 1,
    "user_id": 1,
    "username": "john_doe",
    "email": "john@bennett.edu.in",
    "score": 150,
    "field": "academics",
    "period": "all_time"
  },
  {
    "rank": 2,
    "user_id": 2,
    "username": "jane_doe",
    "email": "jane@bennett.edu.in",
    "score": 140,
    "field": "academics",
    "period": "all_time"
  }
]
```

---

### 25. Get User Rankings
**Endpoint:** `GET /leaderboard/user/{user_id}/`

**Response (200 OK):**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "rankings": [
    {
      "field": "academics",
      "period": "all_time",
      "rank": 1,
      "score": 150
    },
    {
      "field": "sports",
      "period": "monthly",
      "rank": 5,
      "score": 80
    }
  ]
}
```

---

### 26. Calculate Rankings (Admin Only)
**Endpoint:** `POST /rankings/calculate/`
**Headers:** `Authorization: Bearer {admin_access_token}`

**Response (200 OK):**
```json
{
  "message": "Rankings calculated successfully"
}
```

---

### 27. Endorse User Skill
**Endpoint:** `POST /endorsements/`
**Headers:** `Authorization: Bearer {access_token}`

**Request Body:**
```json
{
  "endorsed_user_id": 2,
  "skill": "Python"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "endorser": "john_doe",
  "endorsed_user": "jane_doe",
  "skill": "Python",
  "created_at": "2025-01-20T11:00:00Z"
}
```

---

### 28. Get User Endorsements
**Endpoint:** `GET /endorsements/?user_id={user_id}`

**Response (200 OK):** List of endorsements for user

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Not allowed"
}
```

### 404 Not Found
```json
{
  "error": "User not found"
}
```

---

## Headers Required for Protected Endpoints
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

---

## Notes
- OTP is valid for 10 minutes
- JWT access token expires in 5 minutes (default)
- Only @bennett.edu.in email addresses are allowed for registration
- Users can only edit/delete their own posts and comments
- Leaderboards are calculated based on: likes (2 points) + comments (1 point) per post
