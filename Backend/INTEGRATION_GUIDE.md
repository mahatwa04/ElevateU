# Leaderboard Feature Implementation Guide

## Branch: feature/backend-leaderboard

This guide explains all the new leaderboard files and how to integrate them.

---

## Files Created

### 1. **leaderboard_models.py**
Contains two models:
- `Leaderboard` - Stores user rankings per field
- `LeaderboardUpdate` - Logs ranking changes

**Location:** `engagement/leaderboard_models.py`

### 2. **leaderboard_serializers.py**
Contains DRF serializers for API responses:
- `LeaderboardSerializer` - Full leaderboard data
- `LeaderboardUpdateSerializer` - Update history
- `LeaderboardListSerializer` - Simplified list view
- `UserLeaderboardStatsSerializer` - User stats
- `LeaderboardTimeSeriesSerializer` - Time-based rankings

**Location:** `engagement/leaderboard_serializers.py`

### 3. **leaderboard_views.py**
Contains ViewSets for API endpoints:
- `LeaderboardViewSet` - Main leaderboard API
- `LeaderboardUpdateViewSet` - Update history API

**Location:** `engagement/leaderboard_views.py`

### 4. **leaderboard_service.py**
Business logic service class with methods for:
- Calculating scores
- Updating rankings
- Resetting periodic scores
- Getting user stats

**Location:** `engagement/leaderboard_service.py`

### 5. **leaderboard_signals.py**
Django signals that auto-update leaderboard when:
- Like is created/deleted
- Comment is created/deleted
- Follow is created/deleted

**Location:** `engagement/leaderboard_signals.py`

### 6. **leaderboard_urls.py**
URL routing configuration for leaderboard endpoints

**Location:** `engagement/leaderboard_urls.py`

### 7. **leaderboard_tests.py**
Comprehensive test suite:
- Model tests
- Service logic tests
- API endpoint tests

**Location:** `engagement/leaderboard_tests.py`

### 8. **LEADERBOARD_README.md**
Complete documentation of the leaderboard feature

**Location:** `engagement/LEADERBOARD_README.md`

---

## Integration Steps

### Step 1: Update models.py (ADD to existing file)

Add the Leaderboard models to your engagement app. You have two options:

**Option A: Keep in separate file** (Recommended)
- Keep `leaderboard_models.py` separate
- Import in `engagement/__init__.py`

**Option B: Merge into models.py**
- Copy content from `leaderboard_models.py` to end of `engagement/models.py`
- Delete `leaderboard_models.py`

### Step 2: Update engagement/apps.py

Register signals:
```python
from django.apps import AppConfig

class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'
    
    def ready(self):
        import engagement.leaderboard_signals  # Add this line
```

### Step 3: Create Migrations

```powershell
# In backend folder
python manage.py makemigrations engagement
python manage.py migrate
```

This creates tables for:
- `engagement_leaderboard`
- `engagement_leaderboardupdate`

### Step 4: Update engagement/admin.py

Add to the end of file:
```python
from .leaderboard_models import Leaderboard, LeaderboardUpdate

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'score', 'rank', 'updated_at')
    list_filter = ('field', 'rank')
    search_fields = ('user__username', 'field')
    ordering = ('-score',)

@admin.register(LeaderboardUpdate)
class LeaderboardUpdateAdmin(admin.ModelAdmin):
    list_display = ('leaderboard', 'previous_rank', 'new_rank', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('leaderboard__user__username',)
```

### Step 5: Update engagement/urls.py

Replace entire file with:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .leaderboard_views import LeaderboardViewSet, LeaderboardUpdateViewSet

router = DefaultRouter()
# Existing routes (if any)...
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-updates', LeaderboardUpdateViewSet, basename='leaderboard-update')

urlpatterns = [
    path('', include(router.urls)),
]
```

### Step 6: Update elevateu_backend/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('engagement.urls')),  # Add/update this
    path('api/', include('posts.urls')),       # If posts has urls
    path('api/', include('users.urls')),       # If users has urls
]
```

### Step 7: Update Post Model (optional but recommended)

Ensure Post model has `category` field. In `posts/models.py`:
```python
class Post(models.Model):
    ...
    category = models.CharField(max_length=100, blank=True)
    ...
```

Already in your current model ✅

### Step 8: Run Tests

```powershell
# Test the new leaderboard functionality
python manage.py test engagement.leaderboard_tests -v 2
```

---

## Git Workflow

### Create feature branch (if not done)
```powershell
git checkout -b feature/backend-leaderboard
```

### Add files to staging
```powershell
git add engagement/leaderboard_*.py
git add engagement/LEADERBOARD_README.md
git add engagement/apps.py
git add engagement/admin.py
git add engagement/urls.py
```

### Commit
```powershell
git commit -m "feat: add leaderboard system with rankings and scoring"
```

### Push
```powershell
git push origin feature/backend-leaderboard
```

### Create Pull Request
- Go to GitHub repo
- Click "Compare & pull request"
- Add description of changes
- Request review from team

---

## Testing the Feature

### 1. Manual Admin Test
```
1. python manage.py runserver
2. Go to http://localhost:8000/admin/
3. Create a test user
4. Create a test post
5. Create likes/comments
6. Check Leaderboard admin page
```

### 2. API Test with Postman/cURL

```bash
# Get all leaderboards
curl -X GET http://localhost:8000/api/leaderboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get user's stats
curl -X GET http://localhost:8000/api/leaderboard/my-stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get field leaderboard
curl -X GET "http://localhost:8000/api/leaderboard/field/?field=sports" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get weekly rankings
curl -X GET "http://localhost:8000/api/leaderboard/weekly/?field=sports" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Django Shell Test

```bash
python manage.py shell
```

```python
from engagement.leaderboard_service import LeaderboardService
from engagement.leaderboard_models import Leaderboard
from posts.models import Post
from users.models import CustomUser

# Create test user
user = CustomUser.objects.create_user(
    username='testuser',
    email='test@university.edu',
    password='test123',
    field_of_interest='sports'
)

# Create test post
post = Post.objects.create(
    user=user,
    title='Sports Achievement',
    category='sports'
)

# Add scores
LeaderboardService.add_like_score(post.id, 'sports')
LeaderboardService.add_comment_score(post.id, 'sports')
LeaderboardService.add_follow_score(user.id, 'sports')

# Check leaderboard
lb = Leaderboard.objects.get(user=user, field='sports')
print(f"Score: {lb.score}, Rank: {lb.rank}")

# Get stats
stats = LeaderboardService.get_user_stats(user.id)
print(stats)
```

---

## Troubleshooting

### Issue: Import errors
**Solution:** Make sure all files are in the `engagement/` folder

### Issue: Migration conflicts
**Solution:** 
```bash
python manage.py makemigrations --merge
python manage.py migrate
```

### Issue: Signals not triggering
**Solution:** Verify `engagement/apps.py` has `ready()` method

### Issue: Leaderboard not updating
**Solution:** Check that Post has `category` field set

---

## Next Steps

1. ✅ Create files
2. ✅ Run migrations
3. ✅ Run tests
4. ✅ Test API endpoints
5. 📝 Add to PR and merge
6. 🚀 Deploy to staging

---

## Useful Commands

```powershell
# Install/update dependencies
pip install -r requirements.txt

# Run all tests
python manage.py test

# Run only leaderboard tests
python manage.py test engagement.leaderboard_tests

# Create superuser for admin
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Access admin
# Go to http://localhost:8000/admin/
```

---

## File Summary

| File | Purpose | Type |
|------|---------|------|
| leaderboard_models.py | Database models | Models |
| leaderboard_serializers.py | API serializers | Serializers |
| leaderboard_views.py | API endpoints | Views |
| leaderboard_service.py | Business logic | Service |
| leaderboard_signals.py | Auto-updates | Signals |
| leaderboard_urls.py | URL routing | Config |
| leaderboard_tests.py | Test cases | Tests |
| LEADERBOARD_README.md | Documentation | Docs |

---

**Branch:** `feature/backend-leaderboard`  
**Created:** November 2025  
**Status:** Ready for integration

