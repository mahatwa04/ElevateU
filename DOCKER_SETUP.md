# ElevateU Docker Setup Guide

## Overview

This guide provides instructions for running the ElevateU application using Docker and Docker Compose. The setup includes:

- **PostgreSQL Database** - Production-ready relational database
- **Django Backend** - REST API server with gunicorn
- **React Frontend** - Compiled static assets served with Node.js
- **Nginx Reverse Proxy** - Optional production-grade reverse proxy (optional profile)

## Prerequisites

- Docker Desktop (v4.0+)
- Docker Compose (v2.0+)
- macOS, Linux, or Windows (WSL2)

## Quick Start

### 1. Clone and Setup Environment

```bash
cd /Users/mahatwasharma/Desktop/ElevateU

# Copy environment file
cp .env.example .env

# Edit .env with your configuration (optional for development)
# nano .env
```

### 2. Build and Start Services

```bash
# Build all images
docker-compose build

# Start all services in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 3. Verify Services

```bash
# Check all services status
docker-compose ps

# Test backend API
curl http://localhost:8000/api/health/
# Expected response: {"status": "ok"}

# Test frontend
curl http://localhost:5173/
# Should return HTML
```

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000 | REST API endpoints |
| Django Admin | http://localhost:8000/admin | Admin panel |
| Database | localhost:5432 | PostgreSQL (dev only) |

## Database Access

### Via Docker

```bash
# Connect to PostgreSQL container
docker-compose exec db psql -U elevateu_user -d elevateu_db

# Useful SQL commands
\dt                    # List tables
\d table_name         # Describe table
SELECT * FROM auth_user;  # Query users
```

### Via Local Client

```bash
# Install PostgreSQL client (macOS)
brew install postgresql

# Connect
psql -h localhost -U elevateu_user -d elevateu_db
```

## Django Management Commands

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Load fixture data
docker-compose exec backend python manage.py loaddata fixture_name

# Create backup
docker-compose exec db pg_dump -U elevateu_user elevateu_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U elevateu_user elevateu_db < backup.sql
```

## Development Workflows

### Adding a New Python Package

```bash
# 1. Add to Backend/requirements.txt
echo "new-package==1.0.0" >> Backend/requirements.txt

# 2. Rebuild backend image
docker-compose build backend

# 3. Restart service
docker-compose up -d backend
```

### Adding a New NPM Package

```bash
# 1. Add to Frontend/package.json
cd Frontend && npm install new-package && cd ..

# 2. Copy updated package-lock.json
cp Frontend/package-lock.json Frontend/package-lock.json

# 3. Rebuild frontend image
docker-compose build frontend

# 4. Restart service
docker-compose up -d frontend
```

### Running Tests

```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests
docker-compose exec frontend npm test

# With coverage
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report
```

## Environment Configuration

### Development (.env)

```
DEBUG=True
SECRET_KEY=dev-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1
DB_PASSWORD=dev-password
```

### Production (.env)

```
DEBUG=False
SECRET_KEY=<use-django-secret-key-generator>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-secure-password>
ADMIN_PASSWORD=<strong-admin-password>
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000
lsof -i :5173
lsof -i :5432

# Kill process
kill -9 <PID>

# Or change ports in docker-compose.yml
```

### Database Connection Error

```bash
# Check database status
docker-compose logs db

# Rebuild database
docker-compose down -v
docker-compose up -d db
docker-compose exec backend python manage.py migrate
```

### Frontend Build Failure

```bash
# Clear build cache
docker-compose build --no-cache frontend

# Check build logs
docker-compose logs frontend
```

### Permission Denied Errors

```bash
# Fix file permissions
docker-compose exec backend chown -R appuser:appuser /app
```

## Monitoring & Health Checks

```bash
# View real-time stats
docker stats

# Check container health
docker-compose ps

# View health status
docker inspect elevateu_backend | grep -A 15 '"Health"'
```

## Security Considerations

### For Production Deployment:

1. **Change all passwords and secrets**
   - Update `.env` with strong credentials
   - Generate new Django SECRET_KEY

2. **Enable HTTPS**
   - Uncomment nginx service in docker-compose.yml
   - Add SSL certificates to `infra/ssl/`

3. **Database Security**
   - Use managed database service (AWS RDS, Heroku Postgres)
   - Enable connection encryption
   - Regular backups

4. **Image Security**
   - Scan images: `docker scan elevateu_backend`
   - Use non-root users (already configured)
   - Keep base images updated

5. **Network Security**
   - Use private networks for internal services
   - Restrict port access
   - Add WAF rules for nginx

## Cleanup

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: Deletes database)
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Clean up dangling images
docker image prune -a

# Full cleanup
docker system prune -a --volumes
```

## Production Deployment

### Using Nginx Reverse Proxy

```bash
# Start with production profile
docker-compose --profile production up -d

# Create self-signed SSL certificate
docker-compose exec nginx openssl req -x509 -newkey rsa:4096 -nodes \
  -out /etc/nginx/ssl/cert.pem -keyout /etc/nginx/ssl/key.pem -days 365
```

### Cloud Deployment Options

#### 1. Railway.app
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### 2. Render.com
- Connect GitHub repository
- Create Web Service
- Set environment variables
- Deploy

#### 3. DigitalOcean App Platform
- Push code to GitHub
- Create app from repository
- Configure services
- Deploy

#### 4. AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <your-ecr-repo>
docker build -t elevateu_backend Backend/
docker tag elevateu_backend:latest <your-ecr-repo>/elevateu_backend:latest
docker push <your-ecr-repo>/elevateu_backend:latest
```

## Performance Optimization

### Database

```bash
# Enable connection pooling
# Edit Backend/settings.py DATABASES config

# Create indexes
docker-compose exec backend python manage.py dbshell
CREATE INDEX idx_user_username ON auth_user(username);
CREATE INDEX idx_post_author ON posts_post(author_id);
```

### Caching

```bash
# Add Redis for caching
# Add to docker-compose.yml:
# redis:
#   image: redis:7-alpine
#   ports:
#     - "6379:6379"
```

### Frontend

```bash
# Analyze bundle size
docker-compose exec frontend npm run build -- --analyze

# Optimize images
# Use CDN for static assets
# Enable compression in nginx
```

## Backup & Restore

```bash
# Backup everything
docker-compose exec db pg_dump -U elevateu_user elevateu_db > backup.sql
docker cp elevateu_backend:/app/media ./media_backup

# Restore database
docker-compose exec -T db psql -U elevateu_user elevateu_db < backup.sql

# Restore media files
docker cp media_backup elevateu_backend:/app/media
```

## Useful Commands Reference

```bash
# View all running containers
docker-compose ps -a

# View service logs (last 50 lines)
docker-compose logs --tail=50 backend

# Execute shell commands
docker-compose exec backend bash
docker-compose exec db bash

# Restart specific service
docker-compose restart backend

# Remove service and data
docker-compose rm -v backend

# Rebuild without cache
docker-compose build --no-cache

# View resource usage
docker stats --no-stream
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [React Production Build](https://vitejs.dev/guide/build.html)

---

**Last Updated:** November 20, 2025  
**Status:** Production Ready ✅
