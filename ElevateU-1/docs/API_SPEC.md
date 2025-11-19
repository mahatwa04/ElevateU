# API Specification for ElevateU

## Overview
The ElevateU API allows university students to post their achievements, interact with others through likes and comments, and view rankings and leaderboards based on their contributions. This document outlines the available endpoints, request/response formats, and authentication requirements.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints require authentication via JWT tokens. Users must log in to receive a token, which should be included in the `Authorization` header as follows:
```
Authorization: Bearer <token>
```

## Endpoints

### User Authentication

#### Signup
- **POST** `/auth/signup/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "string",
    "username": "string"
  }
  ```
- **Response**:
  - **201 Created**: User created successfully.
  - **400 Bad Request**: Validation errors.

#### Login
- **POST** `/auth/login/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Response**:
  - **200 OK**: Returns JWT token.
  - **401 Unauthorized**: Invalid credentials.

### Achievements

#### Create Achievement
- **POST** `/achievements/`
- **Request Body**:
  ```json
  {
    "title": "Achievement Title",
    "description": "Description of the achievement",
    "media": "url_to_media",
    "field": "academic/sports/music/dance"
  }
  ```
- **Response**:
  - **201 Created**: Achievement created successfully.
  - **400 Bad Request**: Validation errors.

#### List Achievements
- **GET** `/achievements/`
- **Response**:
  - **200 OK**: Returns a list of achievements.
  ```json
  [
    {
      "id": 1,
      "title": "Achievement Title",
      "description": "Description",
      "media": "url_to_media",
      "field": "academic",
      "likes": 10,
      "comments_count": 5
    }
  ]
  ```

### Engagement

#### Like Achievement
- **POST** `/achievements/{id}/like/`
- **Response**:
  - **200 OK**: Achievement liked successfully.
  - **404 Not Found**: Achievement does not exist.

#### Comment on Achievement
- **POST** `/achievements/{id}/comments/`
- **Request Body**:
  ```json
  {
    "content": "This is a comment."
  }
  ```
- **Response**:
  - **201 Created**: Comment added successfully.
  - **404 Not Found**: Achievement does not exist.

### Rankings

#### Get Rankings
- **GET** `/rankings/`
- **Response**:
  - **200 OK**: Returns rankings based on likes and comments.
  ```json
  [
    {
      "user": "username",
      "field": "academic",
      "rank": 1,
      "score": 100
    }
  ]
  ```

### Leaderboards

#### Get Leaderboard
- **GET** `/leaderboard/`
- **Response**:
  - **200 OK**: Returns leaderboard data.
  ```json
  [
    {
      "user": "username",
      "field": "sports",
      "score": 150
    }
  ]
  ```

## Error Handling
All error responses will include a status code and a message detailing the error.

## Conclusion
This API specification provides a comprehensive overview of the endpoints available in the ElevateU project, facilitating interaction between users and the platform.