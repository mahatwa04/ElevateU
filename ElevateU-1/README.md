# ElevateU

ElevateU is a platform designed for university students to showcase their achievements across various fields, including academics, sports, arts, and more. The website allows users to post their accomplishments, interact with peers through likes and comments, and follow each other to stay updated on their achievements. 

## MVP Features
- **Signup/Login**: Users can register and log in using their university email addresses.
- **Post Achievements**: Students can share their achievements in different formats, including photos and videos.
- **Like/Comment/Follow**: Users can engage with posts by liking, commenting, and following other users.
- **Field-Based Rankings**: Achievements are ranked based on likes and comments, fostering healthy competition among peers.
- **Leaderboards**: Display weekly, monthly, and all-time rankings to highlight top achievers.
- **Skill Tags & Endorsements**: Users can tag their achievements with relevant skills and receive endorsements from peers.
- **Event & Competition Integration**: Opportunities for students to participate in events and competitions related to their fields.

## Tech Stack
- **Backend**: Django + Django REST Framework (Python)
- **Database**: PostgreSQL
- **Storage**: AWS S3 for media files
- **Frontend**: React or Next.js
- **Asynchronous Tasks**: Celery + Redis
- **Deployment**: Docker, with CI/CD pipelines for continuous integration and deployment

## Project Structure
- **backend/**: Contains the Django API and related configurations.
- **frontend/**: Contains the React/Next.js application for the user interface.
- **infra/**: Contains Docker configurations and deployment scripts.
- **docs/**: Documentation for architecture, API specifications, and contribution guidelines.

## Quick Start
1. Clone the repository: `git clone https://github.com/yourusername/ElevateU.git`
2. Navigate to the backend directory: `cd ElevateU/backend`
3. Set up the virtual environment and install dependencies: 
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Configure environment variables in `.env` based on `.env.example`.
5. Run database migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`

For frontend setup, refer to the `frontend/README.md` for instructions on starting the React application.

## Contributing
We welcome contributions! Please refer to the `docs/CONTRIBUTING.md` for guidelines on how to contribute to the project.