# Code Changes for Existing Files

This file shows exactly what code to add/modify in your existing Django files.

---

## File 1: engagement/apps.py

**Current File Location:** `Backend/engagement/apps.py`

**What to Change:** Add the `ready()` method to register signals

**Original Code:**
```python
from django.apps import AppConfig


class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'
```

**Updated Code:**
```python
from django.apps import AppConfig


class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'
    
    def ready(self):
        """Register signals when app is ready."""
        import engagement.leaderboard_signals  # Import to register signals
```

---

## File 2: engagement/admin.py

**Current File Location:** `Backend/engagement/admin.py`

**What to Change:** Add admin classes for Leaderboard models

**Add to the END of the file:**
```python
from .leaderboard_models import Leaderboard, LeaderboardUpdate


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard."""
    
    list_display = ('user', 'field', 'score', 'rank', 'updated_at')
    list_filter = ('field', 'rank', 'updated_at')
    search_fields = ('user__username', 'user__email', 'field')
    readonly_fields = (
        'score', 'rank', 'weekly_score', 'monthly_score',
        'all_time_score', 'total_likes', 'total_comments',
        'total_follows', 'created_at', 'updated_at'
    )
    ordering = ('-score',)
    
    fieldsets = (
        ('User & Field', {
            'fields': ('user', 'field')
        }),
        ('Scores', {
            'fields': ('score', 'weekly_score', 'monthly_score', 'all_time_score')
        }),
        ('Engagement Counts', {
            'fields': ('total_likes', 'total_comments', 'total_follows')
        }),
        ('Ranking', {
            'fields': ('rank',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'weekly_reset_at', 'monthly_reset_at')
        }),
    )


@admin.register(LeaderboardUpdate)
class LeaderboardUpdateAdmin(admin.ModelAdmin):
    """Admin interface for LeaderboardUpdate."""
    
    list_display = ('leaderboard', 'previous_rank', 'new_rank', 'score_change', 'reason', 'created_at')
    list_filter = ('reason', 'created_at', 'leaderboard__field')
    search_fields = ('leaderboard__user__username', 'reason')
    readonly_fields = ('created_at', 'leaderboard', 'previous_rank', 'new_rank', 'score_change', 'reason', 'post')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Leaderboard Info', {
            'fields': ('leaderboard',)
        }),
        ('Ranking Change', {
            'fields': ('previous_rank', 'new_rank')
        }),
        ('Score Change', {
            'fields': ('score_change', 'reason')
        }),
        ('Related Post', {
            'fields': ('post',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
```

---

## File 3: engagement/urls.py

**Current File Location:** `Backend/engagement/urls.py`

**What to Change:** Add leaderboard routes to URL configuration

**Check if file exists. If it does, update it. If not, create it with this content:**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .leaderboard_views import LeaderboardViewSet, LeaderboardUpdateViewSet

router = DefaultRouter()

# Add existing routes here (if any)
# Example:
# router.register(r'posts', PostViewSet, basename='post')

# Leaderboard routes
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-updates', LeaderboardUpdateViewSet, basename='leaderboard-update')

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## File 4: elevateu_backend/urls.py

**Current File Location:** `Backend/elevateu_backend/urls.py`

**What to Change:** Include engagement URLs in main URL config

**Original Code (probably looks like this):**
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

**Updated Code:**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('engagement.urls')),  # Add this line
    # Add other app URLs as needed:
    # path('api/', include('posts.urls')),
    # path('api/', include('users.urls')),
]
```

---

## File 5: posts/models.py (Optional)

**Current File Location:** `Backend/posts/models.py`

**What to Check:** Verify the Post model has a `category` field

**Expected Field:**
```python
class Post(models.Model):
    ...
    category = models.CharField(max_length=100, blank=True)
    ...
```

✅ **Your current model already has this!** No changes needed.

---

## File 6: users/models.py (Optional)

**Current File Location:** `Backend/users/models.py`

**What to Check:** Verify CustomUser has `field_of_interest` field

**Expected Field:**
```python
class CustomUser(AbstractUser):
    ...
    field_of_interest = models.CharField(max_length=100)
    ...
```

✅ **Your current model already has this!** No changes needed.

---

## File 7: elevateu_backend/settings.py (Optional)

**Current File Location:** `Backend/elevateu_backend/settings.py`

**What to Check:** Ensure 'engagement' is in INSTALLED_APPS

**Look for:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps ...
    'engagement',  # Should already be here
]
```

✅ **Your current settings should already have this!** No changes needed.

---

## Summary of Changes

### Files to CREATE (8 Python files + 3 docs):
1. ✅ `engagement/leaderboard_models.py`
2. ✅ `engagement/leaderboard_serializers.py`
3. ✅ `engagement/leaderboard_views.py`
4. ✅ `engagement/leaderboard_service.py`
5. ✅ `engagement/leaderboard_signals.py`
6. ✅ `engagement/leaderboard_urls.py`
7. ✅ `engagement/leaderboard_tests.py`
8. ✅ `engagement/LEADERBOARD_README.md`
9. ✅ `INTEGRATION_GUIDE.md`
10. ✅ `LEADERBOARD_API_REFERENCE.md`

### Files to MODIFY (4 files):
1. ✅ `engagement/apps.py` - Add `ready()` method
2. ✅ `engagement/admin.py` - Add admin classes
3. ✅ `engagement/urls.py` - Add leaderboard routes
4. ✅ `elevateu_backend/urls.py` - Include engagement URLs

### Files to CHECK (2 files - no changes needed):
1. ✅ `posts/models.py` - Already has `category` field
2. ✅ `users/models.py` - Already has `field_of_interest` field

---

## Step-by-Step Integration

### Step 1: Copy new files
```bash
# All 8 .py files to engagement folder
# All 3 .md docs to Backend folder
```

### Step 2: Update engagement/apps.py
Copy the updated `apps.py` code above

### Step 3: Update engagement/admin.py
Add the admin classes at the END of the file

### Step 4: Update engagement/urls.py
Replace entire file with code above

### Step 5: Update elevateu_backend/urls.py
Add the line to include engagement URLs

### Step 6: Run migrations
```bash
python manage.py makemigrations engagement
python manage.py migrate
```

### Step 7: Test
```bash
python manage.py test engagement.leaderboard_tests
python manage.py runserver
```

---

## Verification Checklist

- [ ] All 8 .py files copied to `engagement/`
- [ ] All 3 .md docs copied to `Backend/`
- [ ] `engagement/apps.py` updated with `ready()` method
- [ ] `engagement/admin.py` updated with admin classes
- [ ] `engagement/urls.py` updated with leaderboard routes
- [ ] `elevateu_backend/urls.py` updated to include engagement URLs
- [ ] Migrations created: `python manage.py makemigrations engagement`
- [ ] Migrations applied: `python manage.py migrate`
- [ ] Tests pass: `python manage.py test engagement.leaderboard_tests`
- [ ] Server runs: `python manage.py runserver`
- [ ] Admin pages work: http://localhost:8000/admin/

---

**Ready to integrate!** 🚀

