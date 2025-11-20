# ElevateU Backend

## Overview
ElevateU is a web platform designed for university students to showcase their achievements across various fields such as academics, sports, arts, and more. The platform allows users to post their accomplishments, engage with peers through likes and comments, and follow other users. Additionally, it features a ranking system based on user interactions and leaderboards to highlight top achievers.

## Features
- **Signup/Login**: Users can register and log in using their university email addresses.
- **Post Achievements**: Users can create posts that include photos or videos of their achievements.
- **Engagement**: Users can like, comment on, and follow other users' posts.
- **Field-Based Rankings**: Users are ranked based on likes and comments received in their respective fields.
- **Leaderboards**: Displays rankings for weekly, monthly, and all-time achievements.
- **Skill Tags & Endorsements**: Users can tag their skills and receive endorsements from peers.
- **Event & Competition Integration**: Users can participate in events and competitions to further showcase their talents.

## Tech Stack
- **Backend**: Django + Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Storage**: AWS S3 for media files
- **Frontend**: React or Next.js
- **Asynchronous Tasks**: Celery + Redis
- **Deployment**: Docker, with CI/CD pipelines for continuous integration and deployment

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/ElevateU.git
   cd ElevateU/backend
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in the required values.

5. **Run Migrations**:
   ```
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```
   python manage.py runserver
   ```

## Testing
To run the tests, use:
```
pytest
```

## Contribution
For guidelines on contributing to the project, please refer to the [CONTRIBUTING.md](../docs/CONTRIBUTING.md) file.