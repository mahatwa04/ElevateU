# Production Deployment Configuration for ElevateU

## Backend Deployment (Render)

### Prerequisites
- GitHub account with ElevateU repo access
- Render account (https://render.com)
- PostgreSQL database (Render provides one free tier)

### Steps to Deploy Backend

1. **Connect GitHub to Render**
   ```
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Select your GitHub repo (mahatwa04/ElevateU)
   - Name: elevateu-backend
   - Environment: Python 3.11
   - Build Command: cd Backend && pip install -r requirements.txt && python manage.py collectstatic --noinput
   - Start Command: cd Backend && gunicorn elevateu_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2
   - Plan: Starter (free tier)
   ```

2. **Configure Environment Variables**
   ```
   Add these in Render dashboard → Settings → Environment:
   
   DJANGO_SETTINGS_MODULE=elevateu_backend.settings
   DEBUG=False
   ALLOWED_HOSTS=elevateu-backend.onrender.com
   DJANGO_SECRET_KEY=<generate-random-key-here>
   DATABASE_URL=<postgres://...>  (auto-provided if using Render PostgreSQL)
   CORS_ALLOWED_ORIGINS=https://elevateu-frontend.vercel.app
   AWS_S3_BUCKET=<your-s3-bucket>
   AWS_ACCESS_KEY_ID=<your-aws-key>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret>
   REDIS_URL=<if using Redis>
   ```

3. **Run Migrations on Deployment**
   ```
   In Render → Settings → Advanced:
   - Post Deploy Command: cd Backend && python manage.py migrate
   ```

4. **Health Check**
   ```
   - Endpoint: /api/health/
   - Interval: 10 minutes
   - Timeout: 5 seconds
   ```

5. **Verify Deployment**
   ```bash
   curl https://elevateu-backend.onrender.com/api/health/
   # Expected: {"status": "ok"}
   ```

### Database Setup

**Option A: Use Render PostgreSQL (Recommended)**
```
1. In Render dashboard → "PostgreSQL"
2. Copy DATABASE_URL from environment
3. Add to backend environment variables
4. Run migrations automatically
```

**Option B: External PostgreSQL (e.g., AWS RDS, Railway)**
```
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

---

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub repo access

### Steps to Deploy Frontend

1. **Import Project to Vercel**
   ```
   - Visit https://vercel.com/new
   - Import your GitHub repo
   - Root Directory: Frontend/
   - Build Command: npm run build
   - Output Directory: .next
   ```

2. **Configure Environment Variables**
   ```
   In Vercel Project Settings → Environment Variables:
   
   NEXT_PUBLIC_API_URL=https://elevateu-backend.onrender.com/api
   ```

3. **Deploy**
   ```
   - Click "Deploy"
   - Vercel automatically builds and deploys
   - Get auto-generated URL: elevateu.vercel.app
   ```

4. **Setup Custom Domain** (Optional)
   ```
   - In Vercel → Settings → Domains
   - Add your custom domain
   - Update backend CORS: elevateu.yourdomain.com
   ```

5. **Verify Deployment**
   ```bash
   curl https://elevateu.vercel.app
   # Should see Next.js homepage
   ```

---

## Database Connection

### PostgreSQL Production Setup

1. **Create Database**
   ```sql
   CREATE DATABASE elevateu_db;
   CREATE USER elevateu WITH PASSWORD 'secure_password';
   ALTER ROLE elevateu SET client_encoding TO 'utf8';
   GRANT ALL PRIVILEGES ON DATABASE elevateu_db TO elevateu;
   ```

2. **Run Migrations**
   ```bash
   DATABASE_URL=postgres://elevateu:pass@host:5432/elevateu_db python manage.py migrate
   ```

3. **Create Superuser** (Production)
   ```bash
   DATABASE_URL=postgres://... python manage.py createsuperuser
   ```

---

## Caching Setup (Redis)

### Option 1: Render Redis (Recommended)
```bash
1. In Render dashboard → Create Redis service
2. Copy Redis URL
3. Add to environment: REDIS_URL=<redis-url>
4. Django will auto-detect and use it
```

### Option 2: Railway Redis
```bash
1. Create Redis database on Railway
2. Copy connection string
3. REDIS_URL=redis://user:pass@host:port
```

### Django Cache Configuration
```python
# In settings.py for production:

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        }
    }
}

# Cache timeout for different endpoints
CACHE_TIMEOUT_LEADERBOARD = 3600  # 1 hour
CACHE_TIMEOUT_POSTS = 300         # 5 minutes
CACHE_TIMEOUT_USER_PROFILE = 600  # 10 minutes
```

---

## CDN Setup (CloudFront + S3)

### AWS S3 Bucket Setup
```bash
1. Create S3 bucket: elevateu-media
2. Enable static website hosting
3. Add CORS policy:
   {
     "AllowedHeaders": ["*"],
     "AllowedMethods": ["GET"],
     "AllowedOrigins": ["https://elevateu-backend.onrender.com"],
     "MaxAgeSeconds": 3000
   }
4. Generate AWS access keys
5. Add to backend environment variables
```

### CloudFront Distribution
```bash
1. AWS Console → CloudFront → Create distribution
2. S3 bucket: elevateu-media
3. Origin domain: elevateu-media.s3.amazonaws.com
4. Cache behaviors:
   - Default: 1 hour (images, static)
   - API endpoints: No cache
5. HTTPS enabled (recommended)
```

### Django S3 Configuration
```bash
pip install boto3 django-storages

# In settings.py:
if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'AWS_STORAGE_BUCKET_NAME': os.getenv('AWS_S3_BUCKET'),
                'AWS_S3_REGION_NAME': os.getenv('AWS_S3_REGION'),
                'AWS_S3_CUSTOM_DOMAIN': f"{os.getenv('AWS_S3_BUCKET')}.s3.amazonaws.com",
                'AWS_DEFAULT_ACL': 'public-read',
                'AWS_QUERYSTRING_AUTH': False,
                'URL_EXPIRATION_SECS': 3600,
            }
        }
    }
    STATIC_URL = f"https://{os.getenv('AWS_S3_BUCKET')}.s3.amazonaws.com/static/"
```

---

## Performance Monitoring

### Sentry Setup (Error Tracking)
```bash
pip install sentry-sdk

# In settings.py:
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@sentry.io/<project-id>",
    environment="production",
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
)
```

### New Relic (APM)
```bash
pip install newrelic

# Run with: newrelic-admin run-program gunicorn ...
```

### Django Debug Toolbar (Development Only)
```python
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

---

## End-to-End Testing

### Run Tests Locally
```bash
cd e2e
npm install
npm run test
```

### Run Tests in CI/CD (GitHub Actions)
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: cd e2e && npm install
      - run: npm run test -- --project=chromium
        env:
          BASE_URL: https://elevateu-frontend.vercel.app
          API_URL: https://elevateu-backend.onrender.com/api
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: e2e/playwright-report/
```

---

## Health Checks

### Backend Health Check
```bash
curl https://elevateu-backend.onrender.com/api/health/
# Expected response:
# {"status": "ok", "database": "connected", "timestamp": "2024-01-01T00:00:00Z"}
```

### Frontend Health Check
```bash
curl https://elevateu-frontend.vercel.app
# Expected: HTML with Next.js app
```

### Database Health Check
```bash
psql $DATABASE_URL -c "SELECT 1;"
```

---

## Monitoring & Logging

### View Logs
```bash
# Render logs:
- Visit Render dashboard → elevateu-backend → Logs

# Vercel logs:
- Visit Vercel dashboard → elevateu-frontend → Deployments

# Database logs:
- Render PostgreSQL → Logs
```

### Setup Email Alerts
```
In Render → Settings → Notifications:
- Enable email alerts for failed deploys
- Monitor error rates
```

---

## Scaling Guidelines

| Stage | Render Plan | Vercel Plan | Database |
|-------|-----------|-----------|----------|
| MVP (0-100 users) | Starter | Hobby | PostgreSQL Starter |
| Growth (100-1k) | Standard | Pro | PostgreSQL Standard |
| Scale (1k+ users) | Pro | Pro | PostgreSQL Advanced |

---

## Post-Deployment Checklist

- [ ] Backend API responding at `elevateu-backend.onrender.com/api`
- [ ] Frontend loading at `elevateu.vercel.app`
- [ ] Database migrations completed
- [ ] Admin panel accessible (`/admin`)
- [ ] JWT authentication working
- [ ] CORS configured correctly
- [ ] SSL/TLS certificates installed
- [ ] Health checks passing
- [ ] Error tracking (Sentry) configured
- [ ] Performance monitoring active
- [ ] E2E tests passing in CI/CD
- [ ] Backups scheduled (Database)
- [ ] Custom domain configured (optional)
- [ ] Analytics/Monitoring dashboards setup

---

## Troubleshooting

### Build Failures
```bash
# Check logs in Render/Vercel dashboard
# Common issues:
- Missing environment variables
- Incorrect build commands
- Missing dependencies in requirements.txt
- Python/Node version mismatch
```

### Database Connection Errors
```bash
# Test connection locally:
psql $DATABASE_URL
# If fails: Check DATABASE_URL format and network access

# Render PostgreSQL firewall:
- Ensure IP allowlist includes Render dynos
```

### CORS Issues
```bash
# Update backend CORS setting:
CORS_ALLOWED_ORIGINS=https://elevateu.vercel.app
# Restart backend service
```

### Slow Queries
```bash
# Enable query logging:
LOGGING['loggers']['django.db.backends'] = {'level': 'DEBUG'}

# Check slow query log and add indexes
DATABASES['default']['OPTIONS']['OPTIONS'] = '-c log_min_duration_statement=500'
```

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.2/howto/deployment/
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **GitHub Actions**: https://docs.github.com/en/actions
