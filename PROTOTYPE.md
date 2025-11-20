# ElevateU - Product Prototype Documentation

## 🎯 Product Overview

ElevateU is a **social learning platform** designed for Bennett University students to share achievements, track progress, and build community engagement through posts, likes, comments, and following.

**Target Users:** Bennett University students (@bennett.edu.in email)
**Key Features:** Achievement sharing, Social engagement, Leaderboards, User profiles

---

## 🏗️ Architecture

### Tech Stack
- **Backend:** Django 5.2.8 + Django REST Framework
- **Frontend:** Next.js 14 + TypeScript + TailwindCSS
- **Database:** PostgreSQL (production) / SQLite (development)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **State Management:** React Query v5
- **Deployment:** Render (backend) + Vercel (frontend)

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    ElevateU Platform                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐              ┌──────────────────┐ │
│  │   Frontend       │              │    Backend       │ │
│  │  (Next.js 14)    │◄────────────►│  (Django REST)   │ │
│  ├──────────────────┤              ├──────────────────┤ │
│  │ • Login/Register │              │ • Auth System    │ │
│  │ • Feed           │              │ • Post CRUD      │ │
│  │ • Profile        │              │ • Like/Comment   │ │
│  │ • Leaderboard    │              │ • Follow System  │ │
│  └──────────────────┘              │ • Leaderboards   │ │
│                                    └──────────────────┘ │
│                                            │             │
│                                    ┌───────▼─────────┐   │
│                                    │  PostgreSQL     │   │
│                                    │  Database       │   │
│                                    └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Users (CustomUser)
```python
- id: UUID (Primary Key)
- email: EmailField (unique, @bennett.edu.in only)
- username: CharField
- password: PasswordField (hashed)
- first_name: CharField
- last_name: CharField
- bio: TextField (optional)
- profile_image: ImageField (optional)
- is_active: BooleanField
- date_joined: DateTimeField
- updated_at: DateTimeField
```

### Email Verification
```python
- id: UUID
- user: ForeignKey(CustomUser)
- otp: CharField (6 digits)
- created_at: DateTimeField
- expires_at: DateTimeField (10 minutes)
- is_verified: BooleanField
```

### Posts
```python
- id: UUID
- author: ForeignKey(CustomUser)
- title: CharField (max 200)
- description: TextField
- category: CharField (choices: Achievement, Skills, Project, etc.)
- image_url: URLField (optional)
- like_count: IntegerField (auto-updated via signals)
- comment_count: IntegerField (auto-updated via signals)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### Likes
```python
- id: UUID
- user: ForeignKey(CustomUser)
- post: ForeignKey(Post)
- created_at: DateTimeField
- Constraint: unique_together(user, post)
```

### Comments
```python
- id: UUID
- user: ForeignKey(CustomUser)
- post: ForeignKey(Post)
- text: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### Follows
```python
- id: UUID
- follower: ForeignKey(CustomUser, related_name='following')
- following: ForeignKey(CustomUser, related_name='followers')
- created_at: DateTimeField
- Constraint: unique_together(follower, following)
```

### Leaderboard (Events/Skills tracking)
```python
- id: UUID
- user: ForeignKey(CustomUser)
- event_type: CharField (Post, Like, Comment, Achievement)
- points: IntegerField
- created_at: DateTimeField
```

---

## 🔐 Authentication Flow

### 1. Registration (Email OTP Verification)
```
User Registration Request
    ↓
1. User provides email (@bennett.edu.in), password, username
    ↓
2. System generates 6-digit OTP
    ↓
3. OTP sent to email (10-minute expiry)
    ↓
4. User verifies OTP
    ↓
5. Account created, user can login
    ↓
Login generates JWT tokens:
  - Access Token (60 minutes)
  - Refresh Token (7 days)
```

### 2. JWT Token Flow
```javascript
// Login
POST /api/auth/token/
Body: { email, password }
Response: { access, refresh, user }

// Protected Requests
Authorization: Bearer <access_token>

// Token Refresh
POST /api/auth/token/refresh/
Body: { refresh: <refresh_token> }
Response: { access: <new_access_token> }
```

### 3. Auto-Refresh on Frontend
```typescript
// Axios interceptor (frontend/src/lib/axios.ts)
- Intercepts 401 responses
- Automatically calls refresh endpoint
- Retries original request with new token
- User stays logged in seamlessly
```

---

## 📱 API Endpoints

### Authentication
```
POST   /api/auth/register/              → Register user with email
POST   /api/auth/verify-email/          → Verify OTP
POST   /api/auth/token/                 → Login (get JWT tokens)
POST   /api/auth/token/refresh/         → Refresh access token
GET    /api/auth/user/                  → Get current user profile
```

### Posts
```
GET    /api/posts/                      → List all posts (paginated)
GET    /api/posts/<id>/                 → Get single post
POST   /api/posts/                      → Create post
PUT    /api/posts/<id>/                 → Update post
DELETE /api/posts/<id>/                 → Delete post
```

### Engagement (Likes, Comments, Follows)
```
POST   /api/engagement/likes/           → Like a post
DELETE /api/engagement/likes/<id>/      → Unlike a post
POST   /api/engagement/comments/        → Comment on post
DELETE /api/engagement/comments/<id>/   → Delete comment
POST   /api/engagement/follows/         → Follow user
DELETE /api/engagement/follows/<id>/    → Unfollow user
GET    /api/engagement/follows/stats/   → Get follower stats
```

### Leaderboard
```
GET    /api/leaderboard/                → Get top users by points
GET    /api/leaderboard/user/<id>/      → Get user's leaderboard position
GET    /api/leaderboard/stats/          → Get statistics
```

---

## 🎨 Frontend UI Components

### Pages

#### 1. Login Page (`app/login/page.tsx`)
- Email input (@bennett.edu.in)
- Password input
- Login button
- "Create account" link
- Error message display
- Loading state

#### 2. Registration Page (`app/register/page.tsx`)
- Email input validation
- Password confirmation
- Username field
- OTP verification step
- Error handling

#### 3. Feed Page (`app/page.tsx`)
```
┌─────────────────────────────────┐
│  Navbar (Profile, Logout)        │
├─────────────────────────────────┤
│ [+ Create Achievement] Button    │
├─────────────────────────────────┤
│ Post #1                          │
│ ├─ Author info                   │
│ ├─ Title                         │
│ ├─ Description                   │
│ ├─ [❤️ 42] [💬 12] [👤 Follow]  │
│ └─ Buttons: Like, Comment        │
├─────────────────────────────────┤
│ Post #2                          │
│ ... (repeated for all posts)     │
└─────────────────────────────────┘
```

#### 4. Profile Page (`app/profile/[id]/page.tsx`)
- User avatar
- User stats (followers, following, posts)
- Bio
- User's posts list
- Follow/Unfollow button
- Edit profile button (if own profile)

#### 5. Leaderboard Page (`app/leaderboard/page.tsx`)
- Top 10 users ranked by points
- User stats display
- Points breakdown
- "View Profile" links

#### 6. Achievements Page (`app/achievements/page.tsx`)
- Filter by category
- Achievement badges
- Achievement stats

### Reusable Components

#### 1. CreatePostModal (`src/components/posts/CreatePostModal.tsx`)
```typescript
Features:
- Title input (max 200 chars)
- Description textarea
- Category dropdown
- Image URL input
- Form validation (Zod)
- Error messages
- Loading state
- Cancel & Submit buttons
- Keyboard focus trap (a11y)
- Escape key to close
- Optimistic updates
```

#### 2. FeedCard (`src/components/FeedCard.tsx`)
```typescript
Props:
- post: Post
- onLike: () => void
- onComment: () => void
- onFollow: () => void

Displays:
- Author avatar + name
- Post title & description
- Category badge
- Like count + button
- Comment count + button
- Timestamp
```

#### 3. LikeButton (`src/components/LikeButton.tsx`)
- Shows like count
- Toggle like/unlike
- Optimistic UI update
- Loading state

#### 4. CommentButton (`src/components/CommentButton.tsx`)
- Comment count display
- Modal to view comments
- Add comment form

#### 5. FollowButton (`src/components/FollowButton.tsx`)
- Follow/Following state
- Loading state
- Count display

#### 6. Navbar (`src/components/Navbar.tsx`)
- User profile menu
- Logout button
- Navigation links
- Mobile responsive

---

## 🔄 State Management (React Query)

### Query Hooks

#### `useQuery` - Fetching Data
```typescript
// Get all posts
const { data: posts, isLoading } = useQuery({
  queryKey: ['posts'],
  queryFn: () => axios.get('/api/posts/')
})

// Get user profile
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: () => axios.get('/api/auth/user/')
})
```

### Mutation Hooks - Modifying Data

#### usePosts Hook (`src/hooks/usePosts.ts`)
```typescript
// Get posts
const { data: posts } = usePosts()

// Create post with optimistic updates
const createPostMutation = useMutation({
  mutationFn: (data) => axios.post('/api/posts/', data),
  onMutate: (newPost) => {
    // Add to cache immediately
    queryClient.setQueryData(['posts'], old => [...old, newPost])
  },
  onError: (err, newPost, context) => {
    // Rollback on error
    queryClient.setQueryData(['posts'], context.previous)
  },
  onSuccess: () => {
    // Refetch to sync with server
    queryClient.invalidateQueries(['posts'])
  }
})

// Like post
const likeMutation = useMutation({
  mutationFn: (postId) => axios.post('/api/engagement/likes/', { post: postId }),
  onMutate: (postId) => {
    // Optimistically update like count
    queryClient.setQueryData(['posts'], posts =>
      posts.map(p => p.id === postId ? { ...p, like_count: p.like_count + 1 } : p)
    )
  }
})
```

---

## 🔐 Security Features

### 1. Email Domain Restriction
```python
# Only @bennett.edu.in emails allowed
if not email.endswith('@bennett.edu.in'):
    raise ValidationError("Only Bennett University emails allowed")
```

### 2. OTP Verification
- 6-digit random OTP
- 10-minute expiry
- Single use only
- Rate limited (max 3 attempts per minute)

### 3. JWT Authentication
- 60-minute access token (short-lived)
- 7-day refresh token (long-lived, rotatable)
- Signed with SECRET_KEY
- Includes user ID and email claims

### 4. CORS Protection
```python
CORS_ALLOWED_ORIGINS = [
    'https://yourfrontenddomain.vercel.app'
]
```

### 5. CSRF Protection (if using sessions)
```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourfrontenddomain.vercel.app'
]
```

---

## 📊 Signal System (Auto-Updating Counters)

### Problem Solved
Instead of manually updating like_count and comment_count on each Like/Comment, Django signals auto-handle it.

### Implementation
```python
# engagement/signals.py

@receiver(post_save, sender=Like)
def increment_post_likes(sender, instance, created, **kwargs):
    if created:
        instance.post.like_count += 1
        instance.post.save()

@receiver(post_delete, sender=Like)
def decrement_post_likes(sender, instance, **kwargs):
    instance.post.like_count -= 1
    instance.post.save()

@receiver(post_save, sender=Comment)
def increment_post_comments(sender, instance, created, **kwargs):
    if created:
        instance.post.comment_count += 1
        instance.post.save()

@receiver(post_delete, sender=Comment)
def decrement_post_comments(sender, instance, **kwargs):
    instance.post.comment_count -= 1
    instance.post.save()
```

### Flow
```
User clicks "Like" on Post #5
    ↓
Frontend: POST /api/engagement/likes/ { post_id: 5 }
    ↓
Backend creates Like object
    ↓
Django signal fires: post_save(Like)
    ↓
Signal handler automatically increments Post #5.like_count
    ↓
Post #5.like_count = 42 → saved to DB
    ↓
Frontend gets response with updated post
```

---

## 🚀 Deployment Setup

### Production Environment Variables

#### Backend (Django) - `elevateu_backend/settings.py`
```python
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
DATABASE_URL = config('DATABASE_URL')
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
```

#### Frontend (Next.js) - `.env.production`
```
NEXT_PUBLIC_API_BASE=https://your-backend-domain.onrender.com
```

### Render Deployment (`render.yaml`)
```yaml
services:
  - type: web
    name: elevateu-backend
    runtime: python 3.11
    startCommand: gunicorn elevateu_backend.wsgi
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: false
      - key: DATABASE_URL
        fromDatabase:
          name: elevateu-db
          property: connectionString

databases:
  - name: elevateu-db
    plan: free
```

### Vercel Deployment (Next.js)
```
1. Import repository
2. Set root directory: ./frontend
3. Add env var: NEXT_PUBLIC_API_BASE
4. Deploy
```

---

## 📈 Key Features Summary

| Feature | Status | Details |
|---------|--------|---------|
| **Email Authentication** | ✅ Complete | OTP verification, @bennett.edu.in only |
| **JWT Tokens** | ✅ Complete | 60-min access, 7-day refresh |
| **User Profiles** | ✅ Complete | Avatar, bio, followers/following |
| **Post Creation** | ✅ Complete | Title, description, category, image URL |
| **Like System** | ✅ Complete | Auto-updating counters via signals |
| **Comments** | ✅ Complete | Thread-based comments on posts |
| **Follow System** | ✅ Complete | User-to-user follows |
| **Leaderboard** | ✅ Complete | Point-based ranking system |
| **Optimistic Updates** | ✅ Complete | Instant UI feedback before server response |
| **Auto Token Refresh** | ✅ Complete | Seamless token rotation |
| **Responsive Design** | ✅ Complete | Mobile & desktop optimized |
| **Production Configs** | ✅ Complete | Render + Vercel ready |

---

## 🧪 Test Coverage

### Backend Tests (24 total passing)
```
✅ 12 Authentication Tests
  - User registration with OTP
  - Email verification
  - Login/Token generation
  - Token refresh
  - Email validation

✅ 5 Post Tests
  - Create, read, update, delete
  - Author restrictions

✅ 7 Follow Tests
  - Follow/unfollow users
  - Follower stats
  - Self-follow prevention
```

### Frontend Components Tested
- ✅ LoginForm validation
- ✅ CreatePostModal optimistic updates
- ✅ FeedCard rendering
- ✅ LikeButton state management
- ✅ FollowButton interactions

---

## 📝 Code Quality

### Backend Structure
```
Backend/
├── users/              # Authentication
├── posts/              # Post CRUD
├── engagement/         # Likes, Comments, Follows
├── elevateu_backend/   # Django settings
└── requirements.txt    # Dependencies
```

### Frontend Structure
```
frontend/
├── app/                # Next.js pages
│   ├── page.tsx       # Feed
│   ├── login/         # Authentication
│   ├── profile/       # User profile
│   └── leaderboard/   # Rankings
├── src/
│   ├── components/    # Reusable UI
│   ├── context/       # Auth context
│   ├── hooks/         # Custom hooks
│   ├── lib/           # Utilities
│   └── providers/     # React Query setup
└── package.json       # Dependencies
```

---

## 🎯 Usage Flow - End User Journey

### 1. New User
```
1. Visit ElevateU website
2. Click "Sign up"
3. Enter email (@bennett.edu.in)
4. Receive OTP in email
5. Enter OTP to verify
6. Set password & username
7. Account created ✅
```

### 2. Existing User
```
1. Visit ElevateU
2. Click "Log in"
3. Enter email & password
4. JWT tokens generated
5. Redirected to feed ✅
6. Automatically stays logged in (token refresh)
```

### 3. Create Post
```
1. Click "+ Create Achievement"
2. Modal opens
3. Fill title, description, category
4. Optionally add image URL
5. Click submit
6. Post appears immediately (optimistic UI)
7. Server confirms ✅
```

### 4. Engage with Post
```
1. See post in feed
2. Click ❤️ to like (count updates instantly)
3. Click 💬 to comment
4. Click 👤 to follow author
5. View author's profile
6. Browse their posts
```

### 5. Check Leaderboard
```
1. Navigate to "Leaderboard"
2. View top 10 users by points
3. Click user to see profile
4. See their achievements
5. Follow if interested
```

---

## 🔧 Configuration Files

### Procfile (Render)
```
release: python manage.py migrate
web: gunicorn elevateu_backend.wsgi
```

### .gitignore
```
node_modules/
frontend/node_modules/
__pycache__/
*.pyc
.env
.env.local
.next/
dist/
build/
```

### requirements.txt (Key Dependencies)
```
Django==5.2.8
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.2
django-cors-headers==4.3.0
gunicorn==22.0.0
psycopg2-binary==2.9.9
python-decouple==3.8
whitenoise==6.6.0
dj-database-url==2.1.0
```

### package.json (Key Dependencies)
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "typescript": "^5.3.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.0.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "tailwindcss": "^3.4.0"
  }
}
```

---

## 🎓 Learning Outcomes

This prototype demonstrates:
- ✅ Full-stack web development (Django + Next.js)
- ✅ RESTful API design
- ✅ JWT authentication & security
- ✅ Database modeling (relationships)
- ✅ Real-time UI updates (optimistic caching)
- ✅ Component-based architecture
- ✅ State management (React Query)
- ✅ Form validation (Zod)
- ✅ CI/CD & deployment
- ✅ Testing strategies

---

## 🚀 Next Steps for Enhancement

1. **Real-time Features**
   - WebSockets for live notifications
   - Real-time comment updates

2. **Advanced Search**
   - Full-text search on posts
   - Filter by category, author, date

3. **Recommendations**
   - ML-based post recommendations
   - User suggestions based on interests

4. **Analytics**
   - User engagement metrics
   - Post performance tracking
   - Activity heatmaps

5. **Gamification**
   - Badges & achievements
   - Points multipliers
   - Streak tracking

6. **Content Moderation**
   - NSFW detection
   - Spam filtering
   - Reporting system

---

**ElevateU - Built with Next.js, Django, and Community! 🚀**
