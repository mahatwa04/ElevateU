# Quick Start: Deploy ElevateU on Render

## 5-Minute Setup

### Step 1: Go to Render Dashboard
1. Login to [render.com](https://render.com)
2. Click **New +** → **Web Service**

### Step 2: Connect GitHub
- Select **Deploy existing repository**
- Choose **mahatwa04/ElevateU**
- Select branch: **deployment-ready**
- Click **Connect**

### Step 3: Configure Service
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `elevateu-backend` |
| **Environment** | Python 3 |
| **Region** | us-east-1 (or closest to you) |
| **Build Command** | `pip install -r Backend/requirements.txt && cd Backend && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `cd Backend && gunicorn elevateu_backend.wsgi:application` |

### Step 4: Add Environment Variables
Click **Add Environment Variable** for each:

```
SECRET_KEY = (click "Generate" button - it will create a random secure key)
DEBUG = False
ALLOWED_HOSTS = <your-service-name>.onrender.com
```

### Step 5: Create Database
1. Click **New +** → **PostgreSQL**
2. Fill in:
   - **Name:** elevateu-db
   - **Database:** elevateu_db
   - **User:** elevateu_user
   - **Region:** Same as web service

3. After creation, copy the **CONNECTION_STRING**

### Step 6: Link Database
Back in Web Service settings:
1. Click **Environment**
2. Add new variable:
   - **Key:** DATABASE_URL
   - **Value:** (paste the CONNECTION_STRING from step 5)

### Step 7: Deploy
- Click **Create Web Service**
- Render will automatically deploy (watch the logs)
- Once deployed, you'll see: "Your service is live"

### Step 8: Test Your API
Visit: `https://<your-service-name>.onrender.com/api/`

You should see the Django REST Framework interface.

---

## After Deployment

### Run Migrations (if needed)
1. Go to **Dashboard** → **Shell** (top right)
2. Run:
   ```bash
   python manage.py migrate
   ```

### Create Admin User
In Shell, run:
```bash
python manage.py createsuperuser
```

Then visit: `https://<your-service-name>.onrender.com/admin/`

---

## Frontend Deployment Options

### Option 1: Vercel (Recommended for HTML/CSS/JS)
1. Create a new Vercel project
2. Point to `frontend/public/` folder
3. Set build output to the public folder

### Option 2: Same Server (Django)
Update CORS settings with your Render service URL

### Option 3: Render Static Site
Create a static site on Render pointing to `frontend/public/`

---

## Important Notes

⚠️ **Ephemeral Storage:**
- Render uses ephemeral storage
- Uploaded images/files are **deleted when service restarts**
- **Solution:** Use Cloudinary, AWS S3, or similar cloud storage

📝 **Free Tier Limitations:**
- Service spins down after 15 min of inactivity (takes ~30s to wake up)
- 0.5GB RAM
- 400MB storage

✅ **What's Ready:**
- Django backend fully configured
- PostgreSQL database ready
- Static file serving with Whitenoise
- CORS configured
- JWT authentication ready

---

## Troubleshooting

**"Build failed"**
- Check logs for errors
- Ensure build command is correct
- Verify all dependencies in requirements.txt

**"Service won't start"**
- Check start command syntax
- Verify Django settings in environment variables
- Check migrations ran successfully

**"500 errors"**
- Check logs: Dashboard → Logs
- Run migrations: use Shell
- Verify DEBUG=False in production

---

## Next Steps

1. ✅ Deploy backend on Render
2. Deploy frontend (Vercel/Netlify/Render)
3. Update CORS_ALLOWED_ORIGINS with frontend URL
4. Test API endpoints
5. Create admin user for dashboard

---

**Full Guide:** See `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions
