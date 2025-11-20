# 🚀 ElevateU Production Deployment - Step-by-Step Execution Guide

**Date:** November 20, 2025  
**Status:** Ready to Deploy  
**Estimated Time:** 45 minutes  
**Target:** Go-live by end of today

---

## 📋 Deployment Checklist & Status

### Phase 1: Backend Deployment (Render) - 5 minutes
- [ ] Create Render account (or login)
- [ ] Connect GitHub repository
- [ ] Create PostgreSQL database
- [ ] Create Web Service for Django
- [ ] Set all environment variables
- [ ] Run post-deploy migrations
- [ ] Verify health endpoint: `GET /api/health/`
- [ ] Confirm database connection

### Phase 2: Frontend Deployment (Vercel) - 5 minutes
- [ ] Create Vercel account (or login)
- [ ] Import GitHub repository
- [ ] Configure root directory: `Frontend/`
- [ ] Set `NEXT_PUBLIC_API_URL` environment variable
- [ ] Trigger deployment
- [ ] Verify frontend loads
- [ ] Test API connectivity from frontend

### Phase 3: Verify & Test (15 minutes)
- [ ] Health check: `GET /api/health/`
- [ ] Login test: POST `/api/auth/login/`
- [ ] Create post test
- [ ] Like/comment test
- [ ] Leaderboard test
- [ ] E2E tests pass
- [ ] No console errors
- [ ] Images/assets load

### Phase 4: Monitoring Setup (10 minutes)
- [ ] Setup Sentry (error tracking)
- [ ] Configure New Relic (APM)
- [ ] Enable Redis (if available)
- [ ] Setup CloudFront CDN (optional)
- [ ] Verify logs streaming

### Phase 5: Go-Live (5 minutes)
- [ ] Announce to team
- [ ] Share production URLs
- [ ] Provide admin credentials
- [ ] Document support contacts
- [ ] Celebrate! 🎉

---

## 🎯 PART 1: BACKEND DEPLOYMENT TO RENDER (5 minutes)

### Step 1.1: Create Render Account

```
1. Open: https://dashboard.render.com
2. If no account: Sign up with GitHub
3. Authorize ElevateU repository
4. You're logged in!
```

### Step 1.2: Create PostgreSQL Database

```
In Render Dashboard:
1. Click "New +" → "PostgreSQL"
2. Settings:
   ├─ Name: elevateu-db
   ├─ Database: elevateu_db
   ├─ User: elevateu
   ├─ Region: (choose Singapore or nearest)
   ├─ Plan: Starter (free)
   └─ Click "Create Database"
3. Wait 1-2 minutes for database to be ready
4. You'll see connection string: postgres://...
5. Copy and save this URL somewhere safe!
```

### Step 1.3: Create Web Service for Backend

```
In Render Dashboard:
1. Click "New +" → "Web Service"
2. Settings:
   ├─ Repository: mahatwa04/ElevateU
   ├─ Branch: main (or feature/backend-posts)
   ├─ Name: elevateu-backend
   ├─ Environment: Python 3.11
   ├─ Region: (same as database)
   ├─ Build Command:
   │  cd Backend && \
   │  pip install -r requirements.txt && \
   │  python manage.py collectstatic --noinput
   │
   ├─ Start Command:
   │  cd Backend && \
   │  gunicorn elevateu_backend.wsgi:application \
   │  --bind 0.0.0.0:$PORT \
   │  --workers 2 \
   │  --timeout 60
   │
   ├─ Plan: Starter (free)
   └─ Click "Create Web Service"
```

### Step 1.4: Add Environment Variables

```
After Web Service is created:
1. Go to: elevateu-backend → Settings → Environment
2. Add these variables (one by one):

Name: DJANGO_SETTINGS_MODULE
Value: elevateu_backend.settings

Name: DEBUG
Value: False

Name: ALLOWED_HOSTS
Value: elevateu-backend.onrender.com

Name: DJANGO_SECRET_KEY
Value: (Generate random: python -c "import secrets; print(secrets.token_urlsafe(32))")
Example: SqG7K-k_yBvZxWq9Kp5LmN2OqRsT8UvW3XyZ4

Name: DATABASE_URL
Value: (Paste the postgres:// URL from Step 1.2)
Example: postgres://elevateu:password@dpg-xxxxx.onrender.com:5432/elevateu_db

Name: CORS_ALLOWED_ORIGINS
Value: https://elevateu.vercel.app

Name: ENVIRONMENT
Value: production

Name: EMAIL_BACKEND
Value: django.core.mail.backends.console.EmailBackend

3. Click "Save"
```

### Step 1.5: Configure Post-Deploy Command

```
In elevateu-backend → Settings:
1. Scroll to "Post Deploy Command"
2. Enter: cd Backend && python manage.py migrate
3. Enable: "Run post-deploy command for every deploy"
4. Click "Save"
```

### Step 1.6: Deploy Backend

```
1. You should see a "Deploy" button at the top
2. Click it (or it auto-deploys based on git)
3. Watch the deployment logs:
   ├─ "Building..." (2-3 minutes)
   ├─ "Running migrations..." (30 seconds)
   └─ "✓ Live" (service is running)
4. You'll get a URL: https://elevateu-backend.onrender.com
```

### Step 1.7: Verify Backend is Working

```bash
# Test health endpoint (should return 200 OK)
curl https://elevateu-backend.onrender.com/api/health/

# Expected response:
# {"status": "ok", "database": "connected", "timestamp": "2024-01-01T00:00:00Z"}

# Test admin access (should return 200 OK)
curl https://elevateu-backend.onrender.com/admin/

# If both work, backend is deployed! ✅
```

**✅ BACKEND DEPLOYED!** → Move to Step 2

---

## 🎨 PART 2: FRONTEND DEPLOYMENT TO VERCEL (5 minutes)

### Step 2.1: Create Vercel Account

```
1. Open: https://vercel.com
2. If no account: Sign up with GitHub
3. Authorize ElevateU repository
4. You're logged in!
```

### Step 2.2: Import Repository

```
In Vercel Dashboard:
1. Click "Add New..." → "Project"
2. Select: mahatwa04/ElevateU (from GitHub)
3. You'll see project import screen
```

### Step 2.3: Configure Project Settings

```
In Import Project screen:
1. Project Name: elevateu-frontend
2. Framework: Next.js (auto-detected)
3. Root Directory: Frontend/
4. Build Command: npm run build
5. Install Command: npm install
6. Output Directory: .next
7. Click "Deploy"
```

### Step 2.4: Wait for Initial Build

```
Vercel will:
1. Clone your repository
2. Install dependencies (npm install)
3. Build Next.js app (npm run build)
4. Deploy to edge network
5. Give you a URL: elevateu-frontend.vercel.app

Wait 2-3 minutes...
You'll see: "✓ Production Deployment Ready"
```

### Step 2.5: Add Environment Variable

```
After initial deployment:
1. Go to: Project Settings → Environment Variables
2. Add:
   Name: NEXT_PUBLIC_API_URL
   Value: https://elevateu-backend.onrender.com/api
   Scope: All (Production, Preview, Development)
3. Click "Save"
```

### Step 2.6: Redeploy with Environment Variables

```
1. Go back to: Deployments tab
2. Find the latest deployment
3. Click the three dots menu → "Redeploy"
4. Wait 1-2 minutes
5. Status should show "✓ Ready"
```

### Step 2.7: Verify Frontend is Working

```bash
# Visit the frontend URL
https://elevateu.vercel.app

# You should see:
✓ Login page loads
✓ No console errors
✓ API URL is set correctly

# To verify in browser:
1. Open DevTools (F12)
2. Go to Console tab
3. You should see NO errors
4. Try navigating around
```

**✅ FRONTEND DEPLOYED!** → Move to Step 3

---

## 🧪 PART 3: VERIFY & TEST PRODUCTION (15 minutes)

### Step 3.1: Test Backend Health

```bash
# Test health endpoint
curl https://elevateu-backend.onrender.com/api/health/

# Should return:
# HTTP 200
# {"status": "ok", "database": "connected"}

# If you get error:
# - Check Render logs
# - Verify DATABASE_URL is correct
# - Check ALLOWED_HOSTS includes backend URL
```

### Step 3.2: Test Login Flow

```bash
# Test login endpoint
curl -X POST https://elevateu-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@bennett.edu.in",
    "password": "admin123456"
  }'

# Expected response (HTTP 200):
# {
#   "access": "eyJ0eXAiOiJKV1QiLC...",
#   "refresh": "eyJ0eXAiOiJKV1QiLC...",
#   "user": {
#     "id": 1,
#     "email": "admin@bennett.edu.in",
#     "first_name": "Admin"
#   }
# }

# If you get 401 or error:
# - Check admin credentials (see below)
# - Check database migrations ran
# - Check DATABASE_URL connectivity
```

### Step 3.3: Create Admin User (If Needed)

```bash
# SSH into Render backend:
1. Go to Render dashboard → elevateu-backend
2. Click "Connect" tab
3. Copy the shell command
4. Run it locally (or use Render web shell)

# Then create superuser:
python manage.py createsuperuser --email=admin@bennett.edu.in

# Or use existing admin:
# Email: admin@bennett.edu.in
# Password: admin123456
```

### Step 3.4: Test Frontend Login

```
1. Visit: https://elevateu.vercel.app
2. You should see login page
3. Enter credentials:
   Email: admin@bennett.edu.in
   Password: admin123456
4. Click Login
5. You should see: Dashboard/Feed page
6. Navigation should work (Achievements, Leaderboard, Profile)
```

### Step 3.5: Test Key Features

```
In Frontend:
1. ✅ Login works
2. ✅ Can view feed
3. ✅ Can navigate pages
4. ✅ Can create post
5. ✅ Can like/comment
6. ✅ Leaderboard shows rankings
7. ✅ Profile page works
```

### Step 3.6: Run E2E Tests Against Production

```bash
# Update e2e/playwright.config.ts if needed:
baseURL: 'https://elevateu.vercel.app'

# Run tests:
cd e2e
npm install
npm run test

# Expected: 80%+ tests pass
# If tests fail:
# - Check API_URL in environment
# - Verify backend is responding
# - Check CORS configuration
```

### Step 3.7: Monitor Render & Vercel Logs

```
Render Logs:
1. Go to elevateu-backend → Logs
2. Look for errors or warnings
3. Should see: "✓ Listening on..." messages

Vercel Logs:
1. Go to Deployments → Latest → View Logs
2. Look for build or runtime errors
3. Should see: "✓ Deployment successful" messages
```

**✅ PRODUCTION VERIFIED!** → Move to Step 4

---

## 📊 PART 4: ENABLE MONITORING & CACHING (10 minutes)

### Step 4.1: Setup Sentry (Error Tracking)

```
1. Visit: https://sentry.io
2. Sign up with email or GitHub
3. Create new project: Python → Django
4. Copy the DSN (looks like: https://xxxxx@sentry.io/xxxxx)
5. Add to Render environment:
   Name: SENTRY_DSN
   Value: (paste the DSN)
6. Redeploy backend service
```

### Step 4.2: Setup New Relic (APM) - Optional

```
1. Visit: https://newrelic.com/signup
2. Create account
3. Get license key from settings
4. Add to requirements.txt: newrelic==8.x.x
5. Update Start Command to:
   newrelic-admin run-program gunicorn ...
6. Add to Render environment:
   Name: NEW_RELIC_LICENSE_KEY
   Value: (paste the key)
```

### Step 4.3: Enable Redis Caching - Optional

```
If you want faster leaderboard queries:

1. In Render dashboard → New + → Redis
2. Name: elevateu-cache
3. Plan: Starter (free)
4. Copy Redis URL
5. Add to environment:
   Name: REDIS_URL
   Value: (paste URL)
6. Redeploy backend
```

### Step 4.4: Setup CloudFront CDN - Optional

```
For faster static asset delivery:

1. AWS Console → S3 → Create bucket: elevateu-media
2. AWS Console → CloudFront → Create distribution
3. Point to S3 bucket
4. Update Django to use CloudFront
5. Images will load ~80% faster globally
```

**✅ MONITORING ENABLED!** → Move to Step 5

---

## 📢 PART 5: GO-LIVE COMMUNICATION (5 minutes)

### Step 5.1: Share Production URLs

```
Email to team:

Subject: 🎉 ElevateU is Live!

Hi Team,

ElevateU is now live in production!

🌐 Frontend: https://elevateu.vercel.app
🔧 Backend API: https://elevateu-backend.onrender.com/api
📊 Admin Panel: https://elevateu-backend.onrender.com/admin

Credentials:
Email: admin@bennett.edu.in
Password: admin123456

Features:
✅ User authentication (campus email)
✅ Post creation & sharing
✅ Like, comment, follow
✅ Field-based leaderboards
✅ Skill endorsements

Status Dashboard:
- Backend Health: https://elevateu-backend.onrender.com/api/health/
- Error Tracking: (Sentry link)
- Performance Monitoring: (New Relic link)

Please test and report any issues!
```

### Step 5.2: Document Support Contacts

```
Support Process:

Critical Issues:
- Contact: DevOps team
- Escalate: mahatwa04@github.com
- Response: 1 hour

Bug Reports:
- GitHub Issues: https://github.com/mahatwa04/ElevateU/issues
- Slack: #elevateu-bugs
- Response: Next business day

Feature Requests:
- GitHub Discussions: https://github.com/mahatwa04/ElevateU/discussions
- Email: team@elevateu.com
```

### Step 5.3: Setup Monitoring Alerts

```
Render Alerts:
1. elevateu-backend → Alerts
2. Email on: Deploy failures, Service errors
3. Webhook to Slack (optional)

Vercel Alerts:
1. Project Settings → Integrations
2. Add Slack for deployment notifications
3. Enable email alerts

Sentry Alerts:
1. Create alert rules for critical errors
2. Route to Slack #elevateu-alerts
3. Email team on high error rates
```

### Step 5.4: First 24 Hour Checklist

```
Monitor these metrics in first 24 hours:

Render Logs:
- No critical errors
- Response times < 500ms
- Database queries < 100ms

Vercel Analytics:
- Page load time < 2s
- No 5xx errors
- Traffic patterns normal

User Feedback:
- Login working
- Posts loading
- No CORS errors
- Images displaying

Database:
- No connection issues
- Migrations successful
- Data integrity OK
```

**✅ GO-LIVE COMPLETE!** 🎉

---

## 🎯 FINAL VERIFICATION CHECKLIST

```
✅ Backend deployed to Render
✅ Frontend deployed to Vercel
✅ Health check endpoint responding
✅ Login flow working
✅ API connectivity verified
✅ E2E tests passing
✅ Monitoring setup
✅ Team notified
✅ Support documentation ready
✅ Logs being monitored

STATUS: 🟢 LIVE IN PRODUCTION
```

---

## 📞 Quick Support

**If something goes wrong:**

1. Check Render logs
2. Check Vercel logs
3. Test health endpoint
4. Review environment variables
5. Check database connection
6. Verify CORS configuration
7. Look at E2E test results

**Common Issues:**

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check backend logs in Render |
| CORS Error | Verify CORS_ALLOWED_ORIGINS |
| Login fails | Check DATABASE_URL & migrations |
| Images not loading | Check AWS S3 / CloudFront setup |
| Slow queries | Check database indexes & Redis |

---

**Estimated Total Time: 45 minutes**

**Next Steps:**
1. Start with Step 1 (Backend)
2. Follow each step in order
3. Verify at each checkpoint
4. Move to next step only when complete

**You've got this! 🚀**
