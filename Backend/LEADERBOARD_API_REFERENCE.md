# Leaderboard API Quick Reference

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints require JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Get All Leaderboards (Paginated)
```
GET /api/leaderboard/
```
**Query Parameters:**
- `field` (optional): Filter by field (academics, sports, music, dance, art, technology, leadership, other)
- `ordering` (optional): Sort by score, rank, or updated_at (prefix with `-` for descending)
- `search` (optional): Search by username or field

**Example:**
```
GET /api/leaderboard/?field=sports&ordering=-score
```

**Response (200 OK):**
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/leaderboard/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_id": 5,
            "user_username": "john_doe",
            "user_email": "john@university.edu",
            "field": "sports",
            "score": 250,
            "rank": 1,
            "weekly_score": 80,
            "monthly_score": 150,
            "all_time_score": 250,
            "total_likes": 100,
            "total_comments": 25,
            "total_follows": 5,
            "created_at": "2025-11-01T10:00:00Z",
            "updated_at": "2025-11-13T15:30:00Z"
        }
    ]
}
```

---

### 2. Get Specific Leaderboard Entry
```
GET /api/leaderboard/{id}/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "user_id": 5,
    "user_username": "john_doe",
    "user_email": "john@university.edu",
    "field": "sports",
    "score": 250,
    "rank": 1,
    "weekly_score": 80,
    "monthly_score": 150,
    "all_time_score": 250,
    "total_likes": 100,
    "total_comments": 25,
    "total_follows": 5,
    "created_at": "2025-11-01T10:00:00Z",
    "updated_at": "2025-11-13T15:30:00Z"
}
```

---

### 3. Get Field Leaderboard (Top 50)
```
GET /api/leaderboard/field/?field=sports
```

**Query Parameters:**
- `field` (required): Field name

**Response (200 OK):**
```json
{
    "field": "sports",
    "count": 42,
    "leaderboards": [
        {
            "id": 1,
            "username": "john_doe",
            "field": "sports",
            "score": 250,
            "rank": 1,
            "total_likes": 100,
            "total_comments": 25,
            "total_follows": 5
        }
    ]
}
```

---

### 4. Get User's Leaderboards
```
GET /api/leaderboard/user/?user_id=5
```

**Query Parameters:**
- `user_id` (required): User ID

**Response (200 OK):**
```json
{
    "user_id": 5,
    "count": 3,
    "leaderboards": [
        {
            "id": 1,
            "user_id": 5,
            "user_username": "john_doe",
            "field": "sports",
            "score": 250,
            "rank": 1
        },
        {
            "id": 2,
            "user_id": 5,
            "user_username": "john_doe",
            "field": "academics",
            "score": 180,
            "rank": 5
        }
    ]
}
```

---

### 5. Get Current User's Stats
```
GET /api/leaderboard/my-stats/
```

**No Parameters Required**

**Response (200 OK):**
```json
{
    "user_id": 5,
    "username": "john_doe",
    "email": "john@university.edu",
    "field_of_interest": "sports",
    "total_score": 430,
    "average_rank": 3,
    "leaderboards": [
        {
            "id": 1,
            "username": "john_doe",
            "field": "sports",
            "score": 250,
            "rank": 1,
            "total_likes": 100,
            "total_comments": 25,
            "total_follows": 5
        },
        {
            "id": 2,
            "username": "john_doe",
            "field": "academics",
            "score": 180,
            "rank": 5,
            "total_likes": 60,
            "total_comments": 15,
            "total_follows": 2
        }
    ]
}
```

---

### 6. Get Weekly Leaderboard
```
GET /api/leaderboard/weekly/
```

**Query Parameters:**
- `field` (optional): Filter by specific field
- `limit` (optional): Top N users (default: 50)

**Example:**
```
GET /api/leaderboard/weekly/?field=sports&limit=20
```

**Response (200 OK):**
```json
{
    "period": "weekly",
    "field": "sports",
    "leaderboards": [
        {
            "id": 1,
            "username": "john_doe",
            "field": "sports",
            "rank": 1,
            "weekly_score": 80,
            "monthly_score": 150,
            "all_time_score": 250
        }
    ]
}
```

---

### 7. Get Monthly Leaderboard
```
GET /api/leaderboard/monthly/
```

**Query Parameters:**
- `field` (optional): Filter by specific field
- `limit` (optional): Top N users (default: 50)

**Example:**
```
GET /api/leaderboard/monthly/?field=music&limit=15
```

**Response (200 OK):**
```json
{
    "period": "monthly",
    "field": "music",
    "leaderboards": [...]
}
```

---

### 8. Get Top Users by Field
```
GET /api/leaderboard/top-by-field/
```

**Query Parameters:**
- `limit` (optional): Top N users per field (default: 10)

**Example:**
```
GET /api/leaderboard/top-by-field/?limit=5
```

**Response (200 OK):**
```json
{
    "academics": [
        {
            "id": 10,
            "username": "scholar_jane",
            "field": "academics",
            "score": 350,
            "rank": 1
        }
    ],
    "sports": [
        {
            "id": 1,
            "username": "john_doe",
            "field": "sports",
            "score": 250,
            "rank": 1
        }
    ],
    "music": [...],
    "dance": [...],
    "art": [...],
    "technology": [...],
    "leadership": [...],
    "other": [...]
}
```

---

### 9. Get Leaderboard Update History
```
GET /api/leaderboard-updates/
```

**Query Parameters:**
- `ordering` (optional): Sort by created_at (use `-created_at` for newest first)

**Response (200 OK):**
```json
{
    "count": 250,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "leaderboard_field": "sports",
            "leaderboard_user": "john_doe",
            "previous_rank": 2,
            "new_rank": 1,
            "score_change": 5,
            "reason": "follow",
            "post_title": "Amazing Sports Achievement",
            "created_at": "2025-11-13T15:30:00Z"
        }
    ]
}
```

---

### 10. Get Updates for Specific User
```
GET /api/leaderboard-updates/user/?user_id=5
```

**Query Parameters:**
- `user_id` (required): User ID

**Response (200 OK):**
```json
{
    "user_id": 5,
    "updates": [
        {
            "id": 1,
            "leaderboard_field": "sports",
            "leaderboard_user": "john_doe",
            "previous_rank": 3,
            "new_rank": 2,
            "score_change": 2,
            "reason": "comment",
            "post_title": "Great achievement",
            "created_at": "2025-11-13T14:00:00Z"
        }
    ]
}
```

---

### 11. Get Recent Updates
```
GET /api/leaderboard-updates/recent/
```

**Query Parameters:**
- `limit` (optional): Number of recent updates (default: 20)

**Example:**
```
GET /api/leaderboard-updates/recent/?limit=10
```

**Response (200 OK):**
```json
{
    "count": 10,
    "updates": [...]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "field parameter is required"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Server Error
```json
{
    "detail": "Internal server error."
}
```

---

## Field Choices

Valid field values:
- `academics`
- `sports`
- `music`
- `dance`
- `art`
- `technology`
- `leadership`
- `other`

---

## Reason Codes (for updates)

- `like` - Like was added to post
- `comment` - Comment was added to post
- `follow` - User was followed
- `manual` - Manual score adjustment by admin

---

## Scoring Formula

```
Score = (likes × 1) + (comments × 2) + (follows × 5)

Example:
- 10 likes = 10 points
- 5 comments = 10 points
- 2 follows = 10 points
Total = 30 points
```

---

## Common Use Cases

### Get User's Overall Ranking
```bash
curl -X GET http://localhost:8000/api/leaderboard/my-stats/ \
  -H "Authorization: Bearer <token>"
```

### Get Top 5 in Sports
```bash
curl -X GET "http://localhost:8000/api/leaderboard/top-by-field/?limit=5" \
  -H "Authorization: Bearer <token>"
```

### Get Weekly Leaders in Academics
```bash
curl -X GET "http://localhost:8000/api/leaderboard/weekly/?field=academics&limit=10" \
  -H "Authorization: Bearer <token>"
```

### Track Specific User's Progress
```bash
curl -X GET "http://localhost:8000/api/leaderboard/user/?user_id=5" \
  -H "Authorization: Bearer <token>"
```

### View Recent Ranking Changes
```bash
curl -X GET "http://localhost:8000/api/leaderboard-updates/recent/?limit=20" \
  -H "Authorization: Bearer <token>"
```

---

## Pagination

Default page size: 20 items

```
GET /api/leaderboard/?page=2
GET /api/leaderboard/?page=3&page_size=50
```

---

**Last Updated:** November 13, 2025  
**API Version:** 1.0  
**Status:** Active

