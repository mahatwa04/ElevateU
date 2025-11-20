# 🚀 Deploy ElevateU to Production - Step by Step

## Part 1: Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Sign up"
3. Connect your GitHub account
4. Authorize Render

### Step 2: Create Web Service
1. Click "New +" button → "Web Service"
2. Select your repository: `mahatwa04/ElevateU`
3. Fill in these details:
   - **Name:** `elevateu-backend`
   - **Branch:** `Frontend`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r Backend/requirements.txt`
   - **Start Command:** `cd Backend && gunicorn elevateu_backend.wsgi`
   - **Plan:** Free tier (or Starter for always-on)

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Fill in:
   - **Name:** `elevateu-db`
   - **Database:** `elevateu`
   - **User:** `elevateu`
   - **Plan:** Free tier
3. Click "Create Database"
4. Copy the connection string (DATABASE_URL)

### Step 4: Add Environment Variables
Back in Web Service settings, go to "Environment" tab:
```
DEBUG=False
SECRET_KEY=your-secret-key-here (generate at https://djecrety.ir/)
ALLOWED_HOSTS=your-render-url.onrender.com,*.onrender.com
DATABASE_URL=postgresql://... (from Step 3)
CORS_ALLOWED_ORIGINS=https://your-vercel-frontend.vercel.app
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for build (2-3 minutes)
3. Check logs for errors
4. Copy the backend URL (e.g., `https://elevateu-backend.onrender.com`)

### Step 6: Run Migrations
1. In Render dashboard, click "Shell" tab
2. Run:
   ```bash
   cd Backend
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. Create an admin user for testing

---

## Part 2: Deploy Frontend to Vercel (3 minutes)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Install" for GitHub app

### Step 2: Import Project
1. Dashboard → "Add New" → "Project"
2. Select your GitHub repo: `ElevateU`
3. Configuration:
   - **Framework Preset:** Next.js
   - **Root Directory:** `./frontend`

### Step 3: Add Environment Variable
1. Go to Project Settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_API_BASE=https://elevateu-backend.onrender.com
   ```
   (Replace with your actual Render URL from Part 1, Step 5)

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build (1-2 minutes)
3. Get your frontend URL (e.g., `https://elevateu-frontend.vercel.app`)

### Step 5: Update Backend CORS
Go back to Render and update `CORS_ALLOWED_ORIGINS` with your Vercel URL

---

## ✅ Verification Checklist

After deployment, test these URLs:

- [ ] **Backend API:** `https://your-render-url.onrender.com/api/posts/`
  - Should return: `{"detail":"Authentication credentials required."}` or posts list

- [ ] **Admin Panel:** `https://your-render-url.onrender.com/admin/`
  - Login with superuser credentials from Step 6

- [ ] **Frontend:** `https://your-vercel-frontend.vercel.app`
  - Should show login page
  - Can you log in?

- [ ] **API Connection:** 
  - Try registering on frontend
  - Check if backend receives request

---

## 🐛 Troubleshooting

### Backend shows 502 error
- Check logs in Render dashboard
- Verify database is connected (DATABASE_URL set)
- Run migrations in Shell tab

### Frontend can't connect to backend
- Check CORS_ALLOWED_ORIGINS includes your Vercel domain
- Verify NEXT_PUBLIC_API_BASE is correct (no trailing slash)
- Check browser console for errors

### Build fails
- Check that paths are correct (Backend/, frontend/)
- Verify all environment variables are set
- Check requirements.txt and package.json exist

---

## 💡 Important Notes

**Render Free Tier:**
- Services spin down after 15 min of inactivity
- Cold start takes 30 seconds
- To fix: Upgrade to Starter plan ($7/month)

**Vercel Free Tier:**
- Always on (no spin-down)
- Unlimited deployments
- Perfect for frontend

---

## 📊 Cost Estimate (Monthly)

| Service | Free Tier | Starter |
|---------|-----------|---------|
| Render Backend | $0 (sleeps) | $7 |
| Render PostgreSQL | $0 | $15 |
| Vercel Frontend | $0 | $20 |
| **Total** | **$0** | **$42** |

---

## 🎯 Quick Summary

1. **Render Web Service** - Deploy backend (5 min)
2. **Render PostgreSQL** - Create database (2 min)
3. **Vercel** - Deploy frontend (3 min)
4. **Test** - Verify everything works (2 min)

**Total time: ~12 minutes**

---

## 📞 Need Help?

If you get stuck, contact:
- **Render Support:** https://render.com/support
- **Vercel Support:** https://vercel.com/support
- **Check logs:** Always check service logs first

Your code is ready. Just follow these steps and you'll be live! 🎉
