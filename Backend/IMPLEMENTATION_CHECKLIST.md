# Backend Implementation Checklist

## ✅ Completed
- [x] User models (CustomUser, EmailVerification)
- [x] Post models (Post)
- [x] Engagement models (Like, Comment, Follow)
- [x] User registration with email verification (OTP)
- [x] JWT authentication
- [x] Post CRUD operations
- [x] Like/Unlike posts
- [x] Comment on posts
- [x] Follow/Unfollow users
- [x] User profile endpoints
- [x] Leaderboard/Rankings system
- [x] Skill endorsements

## 📋 To-Do: Database Migrations

Run these commands in your Backend folder:

```bash
# Generate migrations for new models
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
```

---

## 📋 To-Do: URL Configuration Updates

Update your `elevateu_backend/urls.py` to include the new endpoints:

```python
from django.contrib import admin
from django.urls import path, include
from core.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),  # NEW: User profile endpoints
    path('api/engagement/', include('engagement.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/', include('core.urls')),  # NEW: Leaderboard & rankings
]
```

---

## 📋 To-Do: Install Missing Dependencies

Check if you have all required packages in `requirements.txt`:

```
Django>=5.0
djangorestframework>=3.15
django-environ>=0.11
django-cors-headers>=4.4
psycopg2-binary>=2.9
gunicorn>=22.0
djangorestframework-simplejwt>=5.3
pillow>=10.0
```

Install missing packages:
```bash
pip install -r requirements.txt
```

---

## 📋 To-Do: Frontend Integration Tasks

### Connect Posts API
```javascript
// Example in frontend
const createPost = async (title, description, category, image) => {
  const response = await fetch('http://localhost:8000/api/posts/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title,
      description,
      category,
      image,
    })
  });
  return response.json();
};
```

### Connect Auth API
```javascript
const register = async (username, email, password, field_of_interest) => {
  const response = await fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      email,
      password,
      password2: password,
      field_of_interest,
    })
  });
  return response.json();
};
```

### Connect Like API
```javascript
const likePost = async (postId, accessToken) => {
  const response = await fetch('http://localhost:8000/api/engagement/likes/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ post: postId })
  });
  return response.json();
};
```

### Connect Leaderboard API
```javascript
const getLeaderboard = async (field = 'academics', period = 'all_time') => {
  const response = await fetch(
    `http://localhost:8000/api/leaderboard/?field=${field}&period=${period}`,
    { headers: { 'Accept': 'application/json' } }
  );
  return response.json();
};
```

---

## 📋 To-Do: Testing APIs with Postman

1. **Import Collection:** Use `ElevateU_Auth_API.postman_collection.json`
2. **Set Base URL:** `http://localhost:8000/api`
3. **Test Endpoints in Order:**
   - Register user
   - Verify email with OTP
   - Login to get tokens
   - Create post
   - Like post
   - Add comment
   - Follow user
   - View leaderboard

---

## 📋 To-Do: Settings Configuration

Ensure these settings in `elevateu_backend/settings.py`:

```python
# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",
]

# JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# Email backend (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 📋 To-Do: Admin Panel Setup

1. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Register models in `admin.py` files:

   **users/admin.py:**
   ```python
   from django.contrib import admin
   from .models import CustomUser, EmailVerification
   
   admin.site.register(CustomUser)
   admin.site.register(EmailVerification)
   ```

   **posts/admin.py:**
   ```python
   from django.contrib import admin
   from .models import Post
   
   admin.site.register(Post)
   ```

   **engagement/admin.py:**
   ```python
   from django.contrib import admin
   from .models import Like, Comment, Follow
   
   admin.site.register(Like)
   admin.site.register(Comment)
   admin.site.register(Follow)
   ```

   **core/admin.py:**
   ```python
   from django.contrib import admin
   from .models_extended import UserFieldRanking, Endorsement
   
   admin.site.register(UserFieldRanking)
   admin.site.register(Endorsement)
   ```

3. Access admin at: `http://localhost:8000/admin`

---

## 📋 To-Do: Run Development Server

```bash
cd /Users/mahatwasharma/Desktop/ElevateU/Backend
python manage.py runserver
```

Server runs at: `http://localhost:8000`

---

## 📋 Testing Checklist

- [ ] Register user with @bennett.edu.in email
- [ ] Verify email with OTP
- [ ] Login and get tokens
- [ ] Create a post
- [ ] Edit own post
- [ ] Delete own post
- [ ] Like someone's post
- [ ] Unlike post
- [ ] Comment on post
- [ ] Update own comment
- [ ] Delete own comment
- [ ] Follow a user
- [ ] Unfollow user
- [ ] View leaderboard
- [ ] Check own rankings
- [ ] Endorse user skill
- [ ] View user endorsements
- [ ] Test pagination
- [ ] Test search/filter

---

## 📋 Files Created/Modified

**New Complete Files:**
- `/posts/views_complete.py` - Enhanced post views with like/comment
- `/posts/serializers_complete.py` - Enhanced serializers
- `/posts/urls_complete.py` - Updated URLs
- `/engagement/views_complete.py` - Like, Comment, Follow views
- `/engagement/serializers_complete.py` - Engagement serializers
- `/engagement/urls_complete.py` - Engagement URLs
- `/users/views_complete.py` - User profile, followers endpoints
- `/core/models_extended.py` - Rankings, Endorsements models
- `/core/views_extended.py` - Leaderboard, Rankings views
- `/core/urls_extended.py` - Leaderboard URLs
- `/API_DOCUMENTATION.md` - Full API docs

**Files to Update (Add imports):**
- `engagement/admin.py` - Register Like, Comment, Follow
- `core/admin.py` - Register UserFieldRanking, Endorsement
- `elevateu_backend/urls.py` - Add new URL includes

---

## 🚀 Next Steps

1. **Run migrations** to create database tables
2. **Test each API endpoint** with Postman
3. **Integrate frontend** with backend APIs
4. **Set up environment variables** (.env file)
5. **Deploy to production** (Render/Railway)

---

## 🐛 Troubleshooting

**Q: Import errors for 'engagement' or 'core'?**
A: Ensure apps are in `INSTALLED_APPS` in settings.py

**Q: OTP not sending?**
A: Check EMAIL_BACKEND in settings. For dev, use 'console' backend.

**Q: CORS errors?**
A: Add frontend URL to CORS_ALLOWED_ORIGINS in settings.py

**Q: 401 Unauthorized on protected endpoints?**
A: Include `Authorization: Bearer {access_token}` header

**Q: Post doesn't show likes_count?**
A: Run `python manage.py migrate` to update Post model

---

## 📞 Support
- Check API_DOCUMENTATION.md for endpoint details
- Review test files for example requests
- Check Django/DRF docs: https://www.django-rest-framework.org/
