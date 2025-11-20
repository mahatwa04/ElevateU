# Leaderboard Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│                    Display Leaderboards                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP Requests
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Django REST API                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ URL Routing (leaderboard_urls.py)                         │ │
│  │ ├─ /api/leaderboard/                                      │ │
│  │ ├─ /api/leaderboard/field/                                │ │
│  │ ├─ /api/leaderboard/weekly/                               │ │
│  │ ├─ /api/leaderboard/monthly/                              │ │
│  │ ├─ /api/leaderboard/my-stats/                             │ │
│  │ └─ /api/leaderboard-updates/                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ViewSets (leaderboard_views.py)                           │ │
│  │ ├─ LeaderboardViewSet                                      │ │
│  │ │  └─ 8 custom actions                                    │ │
│  │ └─ LeaderboardUpdateViewSet                                │ │
│  │    └─ 3 custom actions                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Serializers (leaderboard_serializers.py)                  │ │
│  │ ├─ LeaderboardSerializer                                   │ │
│  │ ├─ LeaderboardUpdateSerializer                             │ │
│  │ ├─ LeaderboardListSerializer                               │ │
│  │ ├─ UserLeaderboardStatsSerializer                          │ │
│  │ └─ LeaderboardTimeSeriesSerializer                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────┬─────────────────────────────┬────────────────────┘
               │                             │
               │ Queries                     │ Updates
               ▼                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ LeaderboardService (leaderboard_service.py)               │ │
│  │                                                            │ │
│  │ Score Management:                                          │ │
│  │ ├─ add_like_score()           → +1 point                 │ │
│  │ ├─ add_comment_score()         → +2 points               │ │
│  │ ├─ add_follow_score()          → +5 points               │ │
│  │                                                            │ │
│  │ Ranking Management:                                        │ │
│  │ ├─ update_rankings()           → recalculate ranks       │ │
│  │ ├─ update_all_rankings()       → all fields              │ │
│  │                                                            │ │
│  │ Periodic Tasks:                                            │ │
│  │ ├─ reset_weekly_scores()       → weekly reset            │ │
│  │ ├─ reset_monthly_scores()      → monthly reset           │ │
│  │                                                            │ │
│  │ Data Retrieval:                                            │ │
│  │ ├─ get_user_stats()            → user overview           │ │
│  │ ├─ get_field_leaders()         → top users in field      │ │
│  │ ├─ get_weekly_leaders()        → weekly rankings         │ │
│  │ └─ get_monthly_leaders()       → monthly rankings        │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────┬────────────────────┬────────────────┬─────────────────┘
           │                    │                │
           │ Triggered by       │ Manages        │ Reads
           │ Signals            │ Scores/Ranks   │ & Returns
           ▼                    ▼                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Signal Layer                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ leaderboard_signals.py                                     │ │
│  │                                                            │ │
│  │ Engagement Events:                                         │ │
│  │ ├─ Like (post_save)                                       │ │
│  │ ├─ Like (post_delete)                                     │ │
│  │ ├─ Comment (post_save)                                    │ │
│  │ ├─ Comment (post_delete)                                  │ │
│  │ ├─ Follow (post_save)                                     │ │
│  │ └─ Follow (post_delete)                                   │ │
│  │                                                            │ │
│  │ Actions:                                                   │ │
│  │ ├─ Update leaderboard scores                              │ │
│  │ ├─ Recalculate ranks                                      │ │
│  │ └─ Log updates (LeaderboardUpdate)                        │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────┬──────────────────┬─────────────────┬─────────────────┘
           │                  │                 │
           │ Save/Delete      │ Create/Update   │ Auto-updates
           │ Operations       │ Scores          │
           ▼                  ▼                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Database Layer                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ engagement_leaderboard                                     │ │
│  │ ├─ id (PK)                                                │ │
│  │ ├─ user_id (FK → auth_user)                              │ │
│  │ ├─ field (choice)                                         │ │
│  │ ├─ score (int)                                            │ │
│  │ ├─ rank (int)                                             │ │
│  │ ├─ weekly_score (int)                                     │ │
│  │ ├─ monthly_score (int)                                    │ │
│  │ ├─ all_time_score (int)                                   │ │
│  │ ├─ total_likes (int)                                      │ │
│  │ ├─ total_comments (int)                                   │ │
│  │ ├─ total_follows (int)                                    │ │
│  │ ├─ created_at (datetime)                                  │ │
│  │ ├─ updated_at (datetime)                                  │ │
│  │ ├─ weekly_reset_at (datetime)                             │ │
│  │ └─ monthly_reset_at (datetime)                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ engagement_leaderboardupdate                              │ │
│  │ ├─ id (PK)                                                │ │
│  │ ├─ leaderboard_id (FK)                                    │ │
│  │ ├─ previous_rank (int)                                    │ │
│  │ ├─ new_rank (int)                                         │ │
│  │ ├─ score_change (int)                                     │ │
│  │ ├─ reason (choice: like/comment/follow/manual)           │ │
│  │ ├─ post_id (FK → posts_post, nullable)                   │ │
│  │ └─ created_at (datetime)                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Existing Models (unchanged)                               │ │
│  │ ├─ auth_user (CustomUser)                                 │ │
│  │ ├─ posts_post (Post)                                      │ │
│  │ ├─ engagement_like (Like)                                 │ │
│  │ ├─ engagement_comment (Comment)                           │ │
│  │ └─ engagement_follow (Follow)                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: User Likes a Post

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User Action: Like Post                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Create Like Record in Database                               │
│    engagement_like (user=5, post=10)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Signal Triggered: post_save(Like)                            │
│    engagement/leaderboard_signals.py                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Service Method Called: add_like_score(post_id=10, field=...)│
│    engagement/leaderboard_service.py                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐      ┌────────────┐     ┌──────────┐
    │ Get/   │      │ Update     │     │ Calculate│
    │Create  │      │ Leaderboard│     │ Rank     │
    │ LB     │      │ Record:    │     │          │
    │        │      │ - scores   │     │ Rank = ? │
    │        │      │ - counts   │     │          │
    └────────┘      └────────────┘     └──────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Database Updates                                             │
│    ├─ Update engagement_leaderboard                            │
│    │  └─ total_likes: 100 → 101                                │
│    │  └─ all_time_score: 150 → 151                             │
│    │  └─ weekly_score: 50 → 51                                 │
│    │  └─ monthly_score: 100 → 101                              │
│    │  └─ rank: 5 → 4 (if score changed)                        │
│    │                                                            │
│    └─ Create engagement_leaderboardupdate                      │
│       └─ reason: 'like'                                        │
│       └─ score_change: +1                                      │
│       └─ previous_rank: 5                                      │
│       └─ new_rank: 4                                           │
│       └─ post_id: 10                                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Frontend Updates                                             │
│    GET /api/leaderboard/my-stats/                              │
│    Returns updated leaderboard data                            │
│    ├─ score: 151                                               │
│    ├─ rank: 4                                                  │
│    └─ total_likes: 101                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Request/Response Flow: API Call

```
┌───────────────────────────────────────────────────────────────┐
│ Frontend: GET /api/leaderboard/weekly/?field=sports&limit=10 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ URLs: leaderboard_urls.py                                    │
│ ├─ Route: /leaderboard/                                      │
│ ├─ ViewSet: LeaderboardViewSet                               │
│ └─ Action: @action weekly()                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ View: leaderboard_views.py                                   │
│ LeaderboardViewSet.weekly(request)                           │
│                                                              │
│ 1. Parse query params: field=sports, limit=10              │
│ 2. Build query: Leaderboard.objects.filter(field='sports')│
│ 3. Order by: -weekly_score                                 │
│ 4. Limit: [:10]                                            │
│ 5. Pass to serializer                                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ Serializer: leaderboard_serializers.py                       │
│ LeaderboardTimeSeriesSerializer(leaderboards, many=True)     │
│                                                              │
│ Convert each Leaderboard object to JSON:                    │
│ {                                                            │
│     "id": 1,                                                │
│     "username": "john_doe",                                 │
│     "field": "sports",                                      │
│     "rank": 1,                                              │
│     "weekly_score": 80,                                     │
│     "monthly_score": 150,                                   │
│     "all_time_score": 250                                   │
│ }                                                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ Response: 200 OK                                             │
│ {                                                            │
│     "period": "weekly",                                     │
│     "field": "sports",                                      │
│     "leaderboards": [                                       │
│         { top 10 entries... }                               │
│     ]                                                        │
│ }                                                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│ Frontend: Render Leaderboard UI                              │
│ ├─ Display period: "Weekly"                                  │
│ ├─ Display field: "Sports"                                   │
│ ├─ Display rankings:                                         │
│ │  Rank 1: john_doe (80 points)                             │
│ │  Rank 2: jane_smith (75 points)                           │
│ │  ... etc                                                   │
│ └─ User can see their position & score                      │
└───────────────────────────────────────────────────────────────┘
```

---

## Score Calculation Flow

```
User Post Achievement
│
├─ Gets 10 Likes
│  └─ Each Like: +1 point
│  └─ Total: 10 points
│
├─ Gets 5 Comments
│  └─ Each Comment: +2 points
│  └─ Total: 10 points
│
├─ Gains 2 New Followers
│  └─ Each Follow: +5 points
│  └─ Total: 10 points
│
└─ TOTAL SCORE = 10 + 10 + 10 = 30 points
   │
   ├─ Added to weekly_score (resets every 7 days)
   ├─ Added to monthly_score (resets every 30 days)
   └─ Added to all_time_score (never resets)

Rank Calculation:
User A: 30 points → Rank 1 (highest)
User B: 25 points → Rank 2
User C: 20 points → Rank 3
... etc
```

---

## Database Schema Relationships

```
┌─────────────────────────┐
│   CustomUser            │
│  (auth_user)            │
├─────────────────────────┤
│ id (PK)                 │
│ username                │
│ email                   │
│ field_of_interest       │
└──────┬──────────────────┘
       │
       ├─ 1:Many → Leaderboard
       ├─ 1:Many → Like
       ├─ 1:Many → Comment
       ├─ 1:Many → Follow
       └─ 1:Many → Post

┌──────────────────────────┐
│   Post (posts_post)      │
├──────────────────────────┤
│ id (PK)                  │
│ user_id (FK)             │
│ title                    │
│ category                 │
│ created_at               │
└──────┬───────────────────┘
       │
       ├─ 1:Many → Like
       ├─ 1:Many → Comment
       └─ 1:Many → LeaderboardUpdate

┌────────────────────────────────────┐
│   Leaderboard (engagement_leaderboard)
├────────────────────────────────────┤
│ id (PK)                            │
│ user_id (FK → CustomUser)          │
│ field (choice)                     │
│ score, rank                        │
│ weekly_score, monthly_score        │
│ all_time_score                     │
│ total_likes, comments, follows     │
└──────┬───────────────────────────────┘
       │
       └─ 1:Many → LeaderboardUpdate

┌────────────────────────────────────┐
│ LeaderboardUpdate (engagement_...)  │
├────────────────────────────────────┤
│ id (PK)                            │
│ leaderboard_id (FK)                │
│ post_id (FK) - nullable            │
│ score_change                       │
│ reason (choice)                    │
│ created_at                         │
└────────────────────────────────────┘
```

---

## Feature Interactions

```
┌─────────────────────────────────────────────────────────────┐
│                   User Interactions                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Action    →  Signal  →  Service  →  Update  →  Log  │
│  ════════════════════════════════════════════════════════  │
│                                                             │
│  Like Post      →  signal  →  add_like   →  +1pt  →  log  │
│  Unlike Post    →  signal  →  -like      →  -1pt  →  log  │
│  Comment        →  signal  →  add_cmnt   →  +2pt  →  log  │
│  Delete Comment →  signal  →  -cmnt      →  -2pt  →  log  │
│  Follow User    →  signal  →  add_follow →  +5pt  →  log  │
│  Unfollow User  →  signal  →  -follow    →  -5pt  →  log  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Weekly Reset (Every Sunday)
│
└─ Celery Task: reset_weekly_leaderboards()
   ├─ Get all Leaderboard objects
   ├─ Check: (now - weekly_reset_at) >= 7 days
   ├─ Reset: weekly_score = 0
   └─ Update: weekly_reset_at = now

Monthly Reset (Every 30 days)
│
└─ Celery Task: reset_monthly_leaderboards()
   ├─ Get all Leaderboard objects
   ├─ Check: (now - monthly_reset_at) >= 30 days
   ├─ Reset: monthly_score = 0
   └─ Update: monthly_reset_at = now

Ranking Update (Every hour)
│
└─ Celery Task: update_all_rankings()
   ├─ For each field:
   │  └─ Sort by score
   │  └─ Assign rank 1, 2, 3...
   │  └─ Update database
   └─ Log changes in LeaderboardUpdate
```

---

## Testing Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Test Cases (leaderboard_tests.py)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Model Tests                                                │
│  ├─ test_leaderboard_creation()                            │
│  ├─ test_calculate_score()                                 │
│  ├─ test_unique_together()                                 │
│  └─ test_leaderboard_update_creation()                     │
│                                                             │
│  Service Tests                                              │
│  ├─ test_add_like_score()                                  │
│  ├─ test_add_comment_score()                               │
│  ├─ test_add_follow_score()                                │
│  ├─ test_update_rankings()                                 │
│  ├─ test_get_user_stats()                                  │
│  ├─ test_reset_weekly_scores()                             │
│  └─ test_reset_monthly_scores()                            │
│                                                             │
│  API Tests                                                  │
│  ├─ test_list_leaderboards()                               │
│  ├─ test_my_stats_endpoint()                               │
│  ├─ test_field_leaderboard()                               │
│  ├─ test_weekly_leaderboard()                              │
│  ├─ test_monthly_leaderboard()                             │
│  ├─ test_top_by_field()                                    │
│  └─ test_update_history_endpoints()                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**This architecture ensures:**
- ✅ Automatic score updates via signals
- ✅ Real-time ranking calculations
- ✅ Scalable API endpoints
- ✅ Comprehensive data logging
- ✅ Easy to test and debug
- ✅ Ready for async tasks (Celery)

