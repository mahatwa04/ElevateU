# ElevateU Render Deployment Guide

## Prerequisites
- A Render account (you already have one)
- Your GitHub repository connected to Render
- PostgreSQL database on Render (free tier available)

## Step-by-Step Deployment

### 1. Create a New Web Service on Render
1. Go to [render.com](https://render.com) and log in
2. Click **New +** → **Web Service**
3. Select **Deploy an existing repository**
4. Choose your **ElevateU** repository from GitHub
5. Click **Connect**

### 2. Configure the Web Service

**Basic Settings:**
- **Name:** `elevateu-backend` (or your preferred name)
- **Environment:** Python 3
- **Region:** Choose closest to you (e.g., us-east-1)
- **Branch:** `deployment-ready`
- **Build Command:** 
  ```bash
  pip install -r Backend/requirements.txt && cd Backend && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command:** 
  ```bash
  cd Backend && gunicorn elevateu_backend.wsgi:application
  ```

### 3. Add Environment Variables

Add these environment variables in the Render dashboard (Settings → Environment):

```
SECRET_KEY=<generate-a-secure-key-here>
DEBUG=False
ALLOWED_HOSTS=<your-render-service>.onrender.com
DATABASE_URL=<will-be-auto-filled-when-you-create-database>
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://<your-frontend-domain>
```

### 4. Create a PostgreSQL Database

1. Click **New +** → **PostgreSQL**
2. **Name:** `elevateu-db`
3. **Database:** `elevateu_db`
4. **User:** `elevateu_user`
5. **Region:** Same as your web service
6. **Plan:** Free tier
7. Click **Create Database**

The DATABASE_URL will be automatically available as an environment variable.

### 5. Connect Database to Web Service

1. Go to your Web Service settings
2. Click **Environment** → **Add Environment Variable**
3. Create a link to the PostgreSQL service by setting:
   - Key: `DATABASE_URL`
   - Value: Select the database service from dropdown

### 6. Deploy Frontend (if needed)

For the frontend (HTML/CSS/JS static files):
- Option A: Deploy to Vercel, Netlify, or GitHub Pages
- Option B: Deploy as a separate Render static site
- Option C: Serve from the same Django server (add to STATIC_ROOT)

### 7. Update CORS Settings

After deploying frontend, update `CORS_ALLOWED_ORIGINS` environment variable with your frontend URL.

## Deployment Steps in Render Dashboard

1. **Web Service Creation:**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure build and start commands

2. **Environment Variables:**
   - Add SECRET_KEY, DEBUG, ALLOWED_HOSTS, etc.

3. **Database Setup:**
   - Create PostgreSQL service
   - Link to web service

4. **Deploy:**
   - Render will automatically deploy when you push to `deployment-ready` branch
   - Check deployment logs in the dashboard

## Troubleshooting

### Static Files Not Loading
- Ensure `STATIC_ROOT` is set correctly
- Run migrations: `python manage.py collectstatic --noinput`

### Database Connection Issues
- Verify DATABASE_URL is set
- Check PostgreSQL service is running
- Run migrations after first deploy

### Media Files Not Uploading
- Media files are stored in `BASE_DIR / 'media'`
- On Render's ephemeral filesystem, files are deleted when service restarts
- Solution: Use cloud storage (AWS S3, Cloudinary, etc.)

### CORS Errors
- Update CORS_ALLOWED_ORIGINS with your frontend URL
- Include http:// or https://

## Production Checklist

- [x] DEBUG set to False
- [x] SECRET_KEY configured
- [x] ALLOWED_HOSTS set correctly
- [x] Database configured
- [x] CORS_ALLOWED_ORIGINS updated
- [x] Static files collection enabled
- [x] Migrations automated

## Useful Commands

After deployment, you can run commands via Render Shell:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Frontend Deployment

For the frontend HTML files in `frontend/public/`, you have options:

1. **Vercel/Netlify:** Push the frontend to a separate repo and deploy there
2. **Render Static Site:** Create a static site service on Render
3. **Same Django Server:** Add frontend files to Django's STATIC_ROOT and serve them

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
