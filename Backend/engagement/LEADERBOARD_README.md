# ElevateU Leaderboard Feature

## Overview

The leaderboard system ranks students based on engagement metrics (likes, comments, follows) in different achievement fields.

---

## Features

✅ **Field-based Rankings** - Separate leaderboards for Academics, Sports, Music, Dance, Art, Technology, Leadership, Other  
✅ **Time-based Rankings** - Weekly, Monthly, and All-time scores  
✅ **Score Calculation** - Weighted engagement: Likes (1pt), Comments (2pts), Follows (5pts)  
✅ **Ranking Updates** - Automatic rank calculation based on scores  
✅ **Update History** - Logs all ranking changes with reasons  
✅ **Real-time Updates** - Signals integrate with Like, Comment, Follow events  

---

## Database Models

### Leaderboard
```python
{
    'id': int,
    'user': User,
    'field': 'academics|sports|music|dance|art|technology|leadership|other',
    'score': int,
    'rank': int,
    'weekly_score': int,
    'monthly_score': int,
    'all_time_score': int,
    'total_likes': int,
    'total_comments': int,
    'total_follows': int,
    'created_at': datetime,
    'updated_at': datetime,
}
```

### LeaderboardUpdate
```python
{
    'id': int,
    'leaderboard': Leaderboard,
    'previous_rank': int,
    'new_rank': int,
    'score_change': int,
    'reason': 'like|comment|follow|manual',
    'post': Post (optional),
    'created_at': datetime,
}
```

---

## API Endpoints

### List All Leaderboards
```
GET /api/leaderboard/
```
Response:
```json
{
    "count": 100,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_id": 5,
            "user_username": "john_doe",
            "user_email": "john@university.edu",
            "field": "sports",
            "score": 250,
            "rank": 1,
            "weekly_score": 80,
            "monthly_score": 150,
            "all_time_score": 250
        }
    ]
}
```

### Get Leaderboard by Field
```
GET /api/leaderboard/field/?field=sports
```

### Get User's Leaderboards
```
GET /api/leaderboard/user/?user_id=5
```

### Get Current User's Stats
```
GET /api/leaderboard/my-stats/
```
Response:
```json
{
    "user_id": 5,
    "username": "john_doe",
    "email": "john@university.edu",
    "field_of_interest": "sports",
    "total_score": 500,
    "average_rank": 3,
    "leaderboards": [
        {
            "id": 1,
            "username": "john_doe",
            "field": "sports",
            "score": 250,
            "rank": 1
        }
    ]
}
```

### Get Weekly Rankings
```
GET /api/leaderboard/weekly/?field=sports&limit=10
```

### Get Monthly Rankings
```
GET /api/leaderboard/monthly/?field=sports&limit=10
```

### Get Top Users by Field
```
GET /api/leaderboard/top-by-field/?limit=10
```
Response:
```json
{
    "academics": [...],
    "sports": [...],
    "music": [...],
    "dance": [...],
    "art": [...],
    "technology": [...],
    "leadership": [...],
    "other": [...]
}
```

### Leaderboard Update History
```
GET /api/leaderboard-updates/
GET /api/leaderboard-updates/user/?user_id=5
GET /api/leaderboard-updates/recent/?limit=20
```

---

## Score Calculation

### Weighting System
- **Like** = 1 point
- **Comment** = 2 points
- **Follow** = 5 points

### Example
```
User A post gets:
- 10 likes = 10 points
- 5 comments = 10 points
- 2 new followers = 10 points
Total = 30 points for that post
```

### Time-based Scores
- **Weekly Score**: Resets every 7 days
- **Monthly Score**: Resets every 30 days
- **All-time Score**: Never resets

---

## Service Methods

### LeaderboardService Class

```python
from engagement.leaderboard_service import LeaderboardService

# Add engagement scores
LeaderboardService.add_like_score(post_id, field)
LeaderboardService.add_comment_score(post_id, field)
LeaderboardService.add_follow_score(user_id, field)

# Update rankings
LeaderboardService.update_rankings(field)  # Single field
LeaderboardService.update_all_rankings()   # All fields

# Reset scores (periodic tasks)
LeaderboardService.reset_weekly_scores()
LeaderboardService.reset_monthly_scores()

# Get data
stats = LeaderboardService.get_user_stats(user_id)
leaders = LeaderboardService.get_field_leaders(field, limit=10)
weekly = LeaderboardService.get_weekly_leaders(field, limit=10)
monthly = LeaderboardService.get_monthly_leaders(field, limit=10)
```

---

## Integration with Engagement Events

### Automatic Updates via Signals

When a user performs these actions, the leaderboard updates automatically:

```python
# In engagement/leaderboard_signals.py
# When Like is created → add 1 point
# When Like is deleted → deduct 1 point
# When Comment is created → add 2 points
# When Comment is deleted → deduct 2 points
# When Follow is created → add 5 points
# When Follow is deleted → deduct 5 points
```

---

## Setup Instructions

### 1. Add to Django Apps
In `elevateu_backend/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'engagement',  # Already installed
]
```

### 2. Create Migrations
```bash
python manage.py makemigrations engagement
python manage.py migrate
```

### 3. Register in Admin
In `engagement/admin.py`:
```python
from django.contrib import admin
from .leaderboard_models import Leaderboard, LeaderboardUpdate

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'score', 'rank', 'updated_at')
    list_filter = ('field', 'rank')
    search_fields = ('user__username', 'field')

@admin.register(LeaderboardUpdate)
class LeaderboardUpdateAdmin(admin.ModelAdmin):
    list_display = ('leaderboard', 'previous_rank', 'new_rank', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
```

### 4. Register URLs
In `elevateu_backend/urls.py`:
```python
from django.urls import path, include
from engagement.leaderboard_urls import urlpatterns as leaderboard_urls

urlpatterns = [
    ...
    path('api/', include(leaderboard_urls)),
]
```

### 5. Setup Signals
In `engagement/apps.py`:
```python
from django.apps import AppConfig

class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'
    
    def ready(self):
        import engagement.leaderboard_signals  # Import signals
```

---

## Testing

Run leaderboard tests:
```bash
python manage.py test engagement.leaderboard_tests
```

Test coverage includes:
- Model creation and validation
- Score calculation
- Ranking updates
- API endpoints
- Signal handling

---

## Periodic Tasks (Celery)

For production, add these Celery tasks:

```python
# engagement/tasks.py
from celery import shared_task
from .leaderboard_service import LeaderboardService

@shared_task
def reset_weekly_leaderboards():
    """Reset weekly scores every Sunday."""
    LeaderboardService.reset_weekly_scores()

@shared_task
def reset_monthly_leaderboards():
    """Reset monthly scores on 1st of each month."""
    LeaderboardService.reset_monthly_scores()

@shared_task
def update_all_rankings():
    """Update all rankings every hour."""
    LeaderboardService.update_all_rankings()
```

---

## Example Scenarios

### Scenario 1: User Posts Achievement in Sports
1. User A posts a sports achievement
2. 10 other users like the post → 10 points added
3. 5 users comment → 10 points added
4. 2 users follow User A → 10 points added
5. **Total: 30 points** → User A moves up in Sports leaderboard

### Scenario 2: Weekly Leaderboard
- Monday-Sunday: Weekly scores accumulate
- Sunday 11:59 PM: Weekly scores reset to 0
- Weekly score still shows in query with param `period=weekly`
- New week starts fresh

### Scenario 3: Multi-field User
- User B is in "Academics" AND "Music"
- Different scores in each field
- Separate ranks in each field
- User A's "all-time score" = sum of all fields

---

## Performance Considerations

### Database Indexes
```python
class Meta:
    indexes = [
        models.Index(fields=['field', '-score']),      # Fast field queries
        models.Index(fields=['user', 'field']),       # Fast user lookups
        models.Index(fields=['leaderboard', '-created_at']),  # Update history
    ]
```

### Query Optimization
- Use `select_related('user')` for API responses
- Cache top 10 leaders per field (Redis)
- Batch update rankings during off-peak hours

---

## Future Enhancements

- [ ] Endorsements from same-major users
- [ ] Achievement badges/milestones
- [ ] Achievements by tag categories
- [ ] Leaderboard streaks (consecutive weeks)
- [ ] Event-based bonus points
- [ ] Skill endorsement multiplier (2x points if endorsed)

