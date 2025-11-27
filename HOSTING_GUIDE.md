# ElevateU Hosting Guide

## Option 1: Deploy Frontend to Vercel (Recommended) ⭐

Vercel is the best platform for Next.js applications and offers free hosting with automatic deployments.

### Step-by-Step:

1. **Go to https://vercel.com**
2. **Click "Sign Up"** → Choose "Continue with GitHub"
3. **Authorize and connect your repository**
4. **Select the ElevateU repository**
5. **Configure the project:**
   - **Framework**: Next.js
   - **Root directory**: `./frontend`
   - **Build command**: `npm run build` (auto-detected)
   - **Output directory**: `.next` (auto-detected)

6. **Add Environment Variable:**
   - Click "Environment Variables"
   - Add: `NEXT_PUBLIC_API_BASE` = `https://elevateu-backend-777j.onrender.com`
   - (Or your production backend URL)

7. **Click "Deploy"** ✅

**Your app will be live at:** `https://your-project-name.vercel.app`

---

## Option 2: Deploy Backend to Render (Already Done!)

Your Django backend is already deployed at:
- **URL**: https://elevateu-backend-777j.onrender.com
- **Admin Panel**: https://elevateu-backend-777j.onrender.com/admin/
- **API Endpoints**: https://elevateu-backend-777j.onrender.com/api/

### Required Environment Variables on Render:
```
SECRET_KEY = django-insecure-9_-x8@!+)@fj0n!8%m@7n8!^n8@7n8!^n8@7n8!^n8@7n8!
DEBUG = False
ALLOWED_HOSTS = elevateu-backend-777j.onrender.com
CORS_ALLOWED_ORIGINS = https://your-vercel-url.vercel.app
DATABASE_URL = (auto-set when PostgreSQL is attached)
```

---

## Option 3: Deploy to GitHub Pages (Frontend Static Export)

If you want to use GitHub Pages instead of Vercel:

### Step 1: Update `next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/ElevateU',
  reactStrictMode: true,
}

module.exports = nextConfig
```

### Step 2: Create GitHub Actions Workflow

Create file: `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [Frontend]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Build
        run: cd frontend && npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/out
          cname: elevateu.bennettuniversity.edu  # (optional custom domain)
```

### Step 3: Enable GitHub Pages
1. Go to repository **Settings** → **Pages**
2. Set **Source**: Deploy from a branch
3. Set **Branch**: `gh-pages`
4. Wait for deployment ✅

**Your app will be live at:** `https://mahatwa04.github.io/ElevateU`

---

## Quick Comparison

| Feature | Vercel | GitHub Pages | Render |
|---------|--------|-------------|--------|
| **Hosting** | Next.js optimized | Static files | Django backend |
| **Cost** | Free tier available | Free | Free tier + paid |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Setup Time** | 5 minutes | 10 minutes | Already done |
| **Recommended** | YES ✅ | Limited (no SSR) | YES ✅ |

---

## What to Do After Deployment

1. **Update Backend CORS** on Render:
   - Go to elevateu-backend service
   - Settings → Environment
   - Update `CORS_ALLOWED_ORIGINS` with your Vercel URL

2. **Test the full stack:**
   - Register at frontend
   - Login with @bennett.edu.in email
   - Verify all API calls work

3. **Set up custom domain** (optional):
   - Vercel: Add domain in settings
   - GitHub Pages: Update CNAME file

---

## Troubleshooting

### "API calls failing on deployed version"
- Check `NEXT_PUBLIC_API_BASE` env variable in Vercel/GitHub Actions
- Verify CORS is configured on Render backend
- Test API directly: `curl https://elevateu-backend-777j.onrender.com/api/posts/`

### "Build fails on Vercel"
- Check build logs in Vercel dashboard
- Ensure `frontend/` directory exists
- Verify `next.config.js` is valid

### "GitHub Pages shows 404"
- Verify GitHub Pages is enabled in repository settings
- Check that branch is set to `gh-pages`
- Wait 1-2 minutes for deployment to complete

---

## Final Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel (or GitHub Pages)
- [ ] Environment variables set
- [ ] CORS configured correctly
- [ ] Database migrations run
- [ ] Admin panel accessible
- [ ] User registration working
- [ ] API calls working from frontend

**Deployment Complete!** 🎉
