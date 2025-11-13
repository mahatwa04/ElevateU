# 🚀 Leaderboard Feature - Quick Start (5 Minutes)

**For:** Person working on backend leaderboard feature  
**Time:** ~5 minutes setup + running code  
**Branch:** `feature/backend-leaderboard`

---

## ⚡ TL;DR (Super Quick)

### 1. All Files Are Already Created ✅

8 Python files + 6 documentation files are in your VS Code workspace:
- `engagement/leaderboard_*.py` (8 files)
- `Backend/*.md` documentation (6 files)

### 2. Copy Files to engagement/ Folder

```powershell
# In VS Code, drag these files to engagement/ folder:
- leaderboard_models.py
- leaderboard_serializers.py
- leaderboard_views.py
- leaderboard_service.py
- leaderboard_signals.py
- leaderboard_urls.py
- leaderboard_tests.py
- LEADERBOARD_README.md
```

### 3. Update 4 Configuration Files

See: `CODE_CHANGES_FOR_EXISTING_FILES.md`

### 4. Run Migrations

```bash
python manage.py makemigrations engagement
python manage.py migrate
```

### 5. Test It

```bash
python manage.py test engagement.leaderboard_tests
python manage.py runserver
# Visit http://localhost:8000/admin/
```

---

## 📋 Step-by-Step (Detailed)

### Step 1: Copy Python Files (3 minutes)

Copy these 8 files to `Backend/engagement/` folder:
- ✅ `leaderboard_models.py`
- ✅ `leaderboard_serializers.py`
- ✅ `leaderboard_views.py`
- ✅ `leaderboard_service.py`
- ✅ `leaderboard_signals.py`
- ✅ `leaderboard_urls.py`
- ✅ `leaderboard_tests.py`

Copy 1 markdown file:
- ✅ `LEADERBOARD_README.md` → to `engagement/`

### Step 2: Update Configuration Files (2 minutes)

#### File 1: engagement/apps.py

Add to the end:
```python
def ready(self):
    import engagement.leaderboard_signals
```

#### File 2: engagement/admin.py

Add to the end:
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

#### File 3: engagement/urls.py

Replace entire file with:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .leaderboard_views import LeaderboardViewSet, LeaderboardUpdateViewSet

router = DefaultRouter()
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-updates', LeaderboardUpdateViewSet, basename='leaderboard-update')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### File 4: elevateu_backend/urls.py

Add this line:
```python
path('api/', include('engagement.urls')),
```

### Step 3: Create Database Tables (1 minute)

```powershell
cd Backend
python manage.py makemigrations engagement
python manage.py migrate
```

### Step 4: Run Tests (1 minute)

```powershell
python manage.py test engagement.leaderboard_tests -v 2
```

Expected output:
```
Ran 20 tests in 0.XXXs
OK
```

### Step 5: Test API (Optional)

```powershell
python manage.py runserver
```

Visit in browser:
- Admin: http://localhost:8000/admin/ (see Leaderboard tables)
- API: http://localhost:8000/api/leaderboard/ (see empty leaderboards)

---

## 📚 Documentation Files

All documentation is pre-written. Just read them:

1. **LEADERBOARD_SUMMARY.md** - Feature overview (start here!)
2. **INTEGRATION_GUIDE.md** - Step-by-step integration
3. **CODE_CHANGES_FOR_EXISTING_FILES.md** - Exact code changes needed
4. **LEADERBOARD_API_REFERENCE.md** - All API endpoints with examples
5. **ARCHITECTURE_DIAGRAMS.md** - System design & data flow
6. **engagement/LEADERBOARD_README.md** - Full feature documentation

---

## 🧪 Test the Feature

### Manual Test (Admin Panel)

1. Go to http://localhost:8000/admin/
2. Login with superuser account
3. Create a user in Users section
4. Create a post in Posts section
5. Create likes/comments
6. Check "Leaderboard" section
7. Verify scores and ranks updated

### API Test

```bash
# Get all leaderboards
curl -X GET http://localhost:8000/api/leaderboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get weekly rankings
curl -X GET "http://localhost:8000/api/leaderboard/weekly/?field=sports" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get your stats
curl -X GET http://localhost:8000/api/leaderboard/my-stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 💾 Commit to Git

```powershell
git add engagement/leaderboard_*.py
git add engagement/LEADERBOARD_README.md
git add Backend/LEADERBOARD_*.md
git add engagement/apps.py
git add engagement/admin.py
git add engagement/urls.py

git commit -m "feat: add leaderboard system with field-based rankings"
git push origin feature/backend-leaderboard
```

---

## ✅ Verification Checklist

- [ ] All 8 .py files copied to `engagement/`
- [ ] All .md docs copied to `Backend/`
- [ ] `apps.py` updated with `ready()` method
- [ ] `admin.py` updated with admin classes
- [ ] `urls.py` updated with leaderboard routes
- [ ] `elevateu_backend/urls.py` updated
- [ ] Migrations created
- [ ] Migrations applied
- [ ] Tests pass
- [ ] API endpoints work
- [ ] Committed to git

---

## 🎯 What You Get

✅ **11 API Endpoints**
- List, filter, search leaderboards
- Time-based rankings (weekly/monthly/all-time)
- User stats and history

✅ **Automatic Score Updates**
- Likes, comments, follows trigger updates
- Via Django signals (no manual code needed)

✅ **Smart Ranking System**
- Ranks users by score per field
- Rank 1 = highest score
- Automatic recalculation

✅ **Complete Testing**
- 20+ test cases included
- Model, service, API tests
- Run with one command

✅ **Full Documentation**
- 1000+ lines of docs
- API reference
- Architecture diagrams
- Integration guide

---

## 🚨 Troubleshooting

### Issue: Import errors after migration
**Fix:** Make sure all .py files are in `engagement/` folder

### Issue: Leaderboard not updating
**Fix:** Verify `apps.py` has `ready()` method with signal import

### Issue: Tests fail
**Fix:** Verify migrations were run: `python manage.py migrate`

### Issue: API returns 404
**Fix:** Verify `elevateu_backend/urls.py` includes engagement URLs

---

## 📞 Quick References

- **Setup:** `CODE_CHANGES_FOR_EXISTING_FILES.md`
- **API:** `LEADERBOARD_API_REFERENCE.md`
- **Features:** `LEADERBOARD_SUMMARY.md`
- **Architecture:** `ARCHITECTURE_DIAGRAMS.md`

---

## ⏱️ Timeline

| Task | Time | Status |
|------|------|--------|
| Copy files | 3 min | ⏳ Do this |
| Update config | 2 min | ⏳ Do this |
| Migrate DB | 1 min | ⏳ Do this |
| Run tests | 1 min | ⏳ Do this |
| Total | **7 min** | 🚀 Ready! |

---

**Ready to build the leaderboard?** Let's go! 🎯

Start with Step 1 above and you'll have a working leaderboard in < 10 minutes!

