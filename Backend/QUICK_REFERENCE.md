# Backend Quick Reference Card

## 🚀 Start Server
```bash
cd /Users/mahatwasharma/Desktop/ElevateU/Backend
python manage.py runserver
```
Access: `http://localhost:8000`  
API Base: `http://localhost:8000/api`  
Admin: `http://localhost:8000/admin`

---

## 🔑 Authentication Headers
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

---

## 📝 User Registration Flow

**1. Register**
```bash
POST /auth/register/
{
  "username": "john",
  "email": "john@bennett.edu.in",
  "password": "Pass123!",
  "password2": "Pass123!",
  "field_of_interest": "academics"
}
```

**2. Get OTP** (Check console output)

**3. Verify Email**
```bash
POST /auth/verify-email/
{
  "email": "john@bennett.edu.in",
  "otp_code": "123456"
}
```
Returns: `access_token` & `refresh_token`

**4. Login**
```bash
POST /auth/token/
{
  "username": "john",
  "password": "Pass123!"
}
```

---

## 📌 Common API Patterns

### Create Resource
```bash
POST /api/{resource}/
Headers: Authorization: Bearer {token}
{
  "field1": "value1",
  "field2": "value2"
}
```

### List Resources
```bash
GET /api/{resource}/?search=query&category=value&ordering=-created_at
```

### Get Single Resource
```bash
GET /api/{resource}/{id}/
```

### Update Resource
```bash
PUT /api/{resource}/{id}/
Headers: Authorization: Bearer {token}
{
  "field1": "new_value"
}
```

### Delete Resource
```bash
DELETE /api/{resource}/{id}/
Headers: Authorization: Bearer {token}
```

---

## 📚 Main Endpoints

| Feature | Endpoint | Auth |
|---------|----------|------|
| Register | POST /auth/register/ | No |
| Verify Email | POST /auth/verify-email/ | No |
| Login | POST /auth/token/ | No |
| User Profile | GET/PUT /users/profile/ | Yes |
| Create Post | POST /posts/ | Yes |
| List Posts | GET /posts/ | No |
| Like Post | POST /engagement/likes/ | Yes |
| Add Comment | POST /engagement/comments/ | Yes |
| Follow User | POST /engagement/follow/ | Yes |
| Leaderboard | GET /leaderboard/ | No |
| Endorsement | POST /endorsements/ | Yes |

---

## 🧪 Quick Test

```bash
# 1. Start server
python manage.py runserver

# 2. In another terminal, run test script
chmod +x API_TEST_SCRIPT.sh
./API_TEST_SCRIPT.sh

# 3. Or use Postman
#    Import: ElevateU_Auth_API.postman_collection.json
```

---

## 🔧 Common Tasks

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Reset Database
```bash
# ⚠️ WARNING: Deletes all data
rm db.sqlite3
python manage.py migrate
```

### Access Admin
```
http://localhost:8000/admin
```

### View Database
```bash
# SQLite: Install DB Browser
# Connect to: db.sqlite3
```

---

## 🔍 Query Parameters

### Leaderboard
```
GET /leaderboard/?field=academics&period=all_time&limit=100

field: academics | sports | music | dance | tech | arts
period: weekly | monthly | all_time
limit: 1-1000
```

### Posts
```
GET /posts/?search=query&category=academics&ordering=-created_at

search: title/description search
category: post category
ordering: created_at | -created_at | likes_count | -likes_count
```

### Comments
```
GET /engagement/comments/?post_id=1
```

### Endorsements
```
GET /endorsements/?user_id=2
```

---

## 📊 Scoring System

**Post Score = (likes × 2) + (comments × 1)**

**User Score in Field = Sum of all post scores in that field**

**Leaderboard Rank = Sorted by score descending**

---

## 🗂️ File Structure

```
Backend/
├── users/
│   ├── models.py (CustomUser, EmailVerification)
│   ├── views.py (existing)
│   ├── views_complete.py (NEW - profile endpoints)
│   ├── serializers.py (existing)
│   └── urls.py
├── posts/
│   ├── models.py
│   ├── views.py (existing)
│   ├── views_complete.py (NEW)
│   ├── serializers_complete.py (NEW)
│   └── urls.py
├── engagement/
│   ├── models.py (Like, Comment, Follow)
│   ├── views.py (existing)
│   ├── views_complete.py (NEW)
│   ├── serializers_complete.py (NEW)
│   └── urls.py
├── core/
│   ├── views.py (health endpoint)
│   ├── models_extended.py (NEW - Rankings, Endorsement)
│   ├── views_extended.py (NEW - Leaderboard)
│   ├── urls_extended.py (NEW)
│   └── urls.py
├── elevateu_backend/
│   ├── settings.py (includes CORS, JWT settings)
│   ├── urls.py (main URL router)
│   └── wsgi.py
├── API_DOCUMENTATION.md (28 endpoints docs)
├── IMPLEMENTATION_CHECKLIST.md (setup guide)
├── BACKEND_SUMMARY.md (overview)
├── API_TEST_SCRIPT.sh (testing script)
├── manage.py
├── requirements.txt
└── db.sqlite3 (created after migrate)
```

---

## ⚡ Environment Variables (.env)

```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

CORS_ALLOWED_ORIGINS=http://localhost:3000
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

JWT_ACCESS_TOKEN_LIFETIME=5  # minutes
JWT_REFRESH_TOKEN_LIFETIME=7  # days
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| Database error | Run `python manage.py migrate` |
| CORS error | Add frontend URL to CORS_ALLOWED_ORIGINS |
| 401 Unauthorized | Add `Authorization: Bearer {token}` header |
| OTP not sent | Check EMAIL_BACKEND (console shows in terminal) |
| Migrations pending | Run `python manage.py migrate` |
| Import errors | Check INSTALLED_APPS in settings.py |

---

## 📱 Frontend Integration Example

```javascript
// API Client
const API_BASE = 'http://localhost:8000/api';

const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers
  };
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });
  
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
};

// Usage
await apiCall('/posts/', {
  method: 'POST',
  body: JSON.stringify({
    title: 'My Achievement',
    description: 'Details here',
    category: 'academics'
  })
});
```

---

## 🎯 Deployment Checklist

- [ ] Update `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure PostgreSQL (not SQLite)
- [ ] Set up environment variables
- [ ] Configure email backend (SMTP)
- [ ] Set ALLOWED_HOSTS
- [ ] Set CORS_ALLOWED_ORIGINS
- [ ] Run `python manage.py collectstatic`
- [ ] Deploy to Render/Railway
- [ ] Set up SSL/HTTPS

---

## 💡 Pro Tips

1. **Always include JWT token** for protected endpoints
2. **Test with Postman** before frontend integration
3. **Check Django logs** for detailed error messages
4. **Use `/api/health/`** to test if server is running
5. **Admin panel** is at `/admin/` (very helpful!)
6. **OTP in console** - check terminal output during dev
7. **Pagination** - add `?limit=10&offset=0` to list endpoints

---

## 🔗 Useful Links

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [JWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Postman](https://www.postman.com/)

---

**Last Updated:** November 20, 2025
**Backend Version:** 1.0
**Status:** Production Ready ✅
