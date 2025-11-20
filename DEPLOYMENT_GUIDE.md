# ElevateU - Production Deployment Guide

Complete step-by-step guide for deploying ElevateU to Render (backend) and Vercel (frontend).

## Prerequisites
- GitHub account with repo pushed to main/Frontend branches
- Render account (render.com) - free tier supported
- Vercel account (vercel.com) - free tier supported
- PostgreSQL knowledge (basic)

## Backend Deployment (Render)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up and connect your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Select your GitHub repo (ElevateU)
3. Fill in:
   - **Name**: elevateu-backend (or custom)
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn elevateu_backend.wsgi`

### Step 3: Configure Environment Variables
Add these variables in Render dashboard:

```
DEBUG=False
SECRET_KEY=<generate-a-random-key-using-django>
ALLOWED_HOSTS=yourdomain.onrender.com,*.onrender.com
CORS_ALLOWED_ORIGINS=https://yourfrontenddomain.vercel.app
```

### Step 4: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: elevateu-db
3. Plan: Free tier (or Starter)
4. Render will auto-populate DATABASE_URL

### Step 5: Deploy
1. Render will auto-build when you push to GitHub
2. Monitor logs in "Logs" tab
3. First build takes 2-3 minutes

### Step 6: Run Migrations
1. Go to "Shell" tab
2. Run: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`

## Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Install Vercel GitHub App

### Step 2: Import Project
1. Dashboard → "Add New..." → "Project"
2. Select your GitHub repo
3. Configure:
   - **Framework**: Next.js
   - **Root Directory**: ./frontend

### Step 3: Add Environment Variable
1. Go to project settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_API_BASE=<your-render-backend-url>
   ```
   Example: `https://elevateu-backend.onrender.com`

### Step 4: Deploy
1. Click "Deploy"
2. Vercel will auto-build
3. Visit your frontend URL when ready

## Verification

### Backend
1. Visit: `https://yourdomain.onrender.com/api/posts/`
2. Should return: `{"detail":"Authentication credentials required."}` or posts list
3. Admin panel: `https://yourdomain.onrender.com/admin/`

### Frontend
1. Visit: `https://yourfrontenddomain.vercel.app`
2. Should see login page
3. Try logging in with created user

## Important Notes

- **Render Free Tier**: Services spin down after 15 min inactivity. For always-on, upgrade to Starter ($7/month)
- **Vercel Free**: Always on, unlimited deployments
- **Database**: PostgreSQL on free tier has limits. Monitor usage in Render dashboard
- **Static Files**: WhiteNoise handles Django static files automatically

## Troubleshooting

### 500 Error on Backend
- Check Render logs for errors
- Verify DATABASE_URL is set correctly
- Run migrations again

### Frontend Can't Connect to Backend
- Verify CORS_ALLOWED_ORIGINS includes your Vercel domain
- Check NEXT_PUBLIC_API_BASE is correct
- No protocol needed if using relative paths

### Build Fails on Render
- Check requirements.txt has all dependencies
- Ensure Procfile is in root directory
- Python version must be 3.11+

## Next Steps
- Monitor logs regularly
- Set up error tracking (Sentry recommended)
- Configure custom domain
- Add SSL certificate (automatic on both platforms)
