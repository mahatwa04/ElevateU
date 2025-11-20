# ElevateU Frontend

A modern React + TypeScript + Vite application for the ElevateU campus achievement sharing platform.

## 🚀 Features

- **Authentication**: Email-based registration and login with OTP verification
- **Post Creation**: Share achievements with images and descriptions
- **Social Engagement**: Like, comment, and follow other users
- **User Profiles**: View user profiles with followers/following lists
- **Leaderboards**: Dynamic leaderboards by field and time period
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: JWT-based authentication with token refresh

## 📁 Project Structure

```
src/
├── components/          # Reusable React components
│   ├── Navbar.tsx       # Navigation bar
│   ├── PostCard.tsx     # Post card component
│   └── Modal.tsx        # Modal dialog component
├── pages/               # Page components
│   ├── LoginPage.tsx    # Login page
│   ├── SignupPage.tsx   # Registration page
│   ├── FeedPage.tsx     # Feed with posts
│   ├── ProfilePage.tsx  # User profile
│   └── LeaderboardPage.tsx # Leaderboards
├── services/            # API integration
│   └── api.ts           # Axios instance and API calls
├── styles/              # CSS files
│   ├── App.css          # Global styles
│   ├── Navbar.css       # Navbar styles
│   ├── AuthPages.css    # Auth page styles
│   ├── FeedPage.css     # Feed page styles
│   ├── PostCard.css     # Post card styles
│   ├── Modal.css        # Modal styles
│   ├── ProfilePage.css  # Profile page styles
│   └── LeaderboardPage.css # Leaderboard styles
├── App.tsx              # Main app component
└── main.tsx             # Application entry point
```

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation Steps

1. **Install Dependencies**
```bash
cd Frontend
npm install
```

2. **Configure Environment**
Create a `.env` file in the Frontend directory:
```
VITE_API_URL=http://localhost:8000/api
```

3. **Start Development Server**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 📚 API Integration

All API calls are centralized in `src/services/api.ts` with:
- Automatic JWT token management
- Request/response interceptors
- Token refresh on expiration
- Error handling

### Usage Example

```typescript
import { authAPI, postAPI, userAPI } from './services/api';

// Login
const response = await authAPI.login(email, password);

// Create post
await postAPI.createPost({ title, description, category, image });

// Get user profile
const profile = await userAPI.getCurrentProfile();
```

## 🎨 UI Components

### Pages
- **LoginPage**: Email/password login with error handling
- **SignupPage**: Two-step registration with field selection
- **FeedPage**: Display posts with create modal
- **ProfilePage**: User profile with followers/following
- **LeaderboardPage**: Filtered leaderboards by field and time

### Components
- **Navbar**: Navigation with logout
- **PostCard**: Post display with actions
- **Modal**: Reusable modal dialog

## 🔐 Authentication Flow

1. User registers with Bennett University email
2. Email OTP verification sent
3. User logs in with email and password
4. JWT tokens stored in localStorage
5. Automatic token refresh on expiration
6. Logout clears tokens

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints: 480px, 600px, 768px, 1024px
- Flexible grid layouts
- Touch-friendly buttons

## 🧪 Testing

Test the application with these flows:

1. **Registration**
   - Sign up with @bennett.edu.in email
   - Verify email with OTP
   - Login with credentials

2. **Posts**
   - Create new post
   - View all posts
   - Like/unlike post
   - Comment on post

3. **Social**
   - Follow/unfollow users
   - View followers/following
   - See user profiles

4. **Leaderboards**
   - Filter by field (Academics, Sports, etc.)
   - Filter by time period (All Time, Monthly, Weekly)
   - See rankings

## 🚀 Building for Production

```bash
# Build the application
npm run build

# Preview production build locally
npm run preview
```

The optimized build will be in the `dist/` directory.

## 📦 Dependencies

- **react**: UI library
- **react-dom**: React DOM rendering
- **react-router-dom**: Client-side routing
- **axios**: HTTP client
- **typescript**: Type safety
- **vite**: Build tool

## 🔧 Development

### Code Style
- TypeScript for type safety
- React functional components with hooks
- CSS modules for styling
- Consistent naming conventions

### Key Features
- Protected routes for authenticated pages
- Error handling with user feedback
- Loading states for async operations
- Form validation
- Token management

## 📖 API Endpoints Reference

### Authentication (4 endpoints)
```
POST /auth/register/         - Register new user
POST /auth/verify-email/     - Verify email with OTP
POST /auth/login/            - Login user
POST /token/refresh/         - Refresh JWT token
```

### Users (5 endpoints)
```
GET  /users/profile/         - Get current user
GET  /users/<id>/            - Get user details
PUT  /users/<id>/            - Update profile
GET  /users/<id>/followers/  - Get followers
GET  /users/<id>/following/  - Get following
```

### Posts (5 endpoints)
```
POST /posts/                 - Create post
GET  /posts/                 - List posts
GET  /posts/<id>/            - Get post details
PUT  /posts/<id>/            - Update post
DELETE /posts/<id>/          - Delete post
```

### Engagement (10+ endpoints)
```
POST   /posts/<id>/like/     - Like post
DELETE /posts/<id>/like/     - Unlike post
POST   /posts/<id>/comments/ - Add comment
GET    /posts/<id>/comments/ - Get comments
POST   /users/<id>/follow/   - Follow user
DELETE /users/<id>/follow/   - Unfollow user
POST   /endorsements/        - Create endorsement
```

### Leaderboards (4 endpoints)
```
GET /leaderboard/            - Get leaderboard
GET /leaderboard/user/<id>/  - Get user rankings
POST /rankings/calculate/    - Calculate rankings
POST /endorsements/          - Create endorsement
```

## 🐛 Troubleshooting

### API Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify API URL in environment variables

### Authentication Issues
- Clear localStorage and retry login
- Check that email is verified
- Ensure JWT tokens are properly stored

### Build Issues
- Delete `node_modules` and `dist` folders
- Run `npm install` again
- Check TypeScript errors with `npm run type-check`

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

1. Create feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Submit pull request

## 📞 Support

For issues and questions, contact the ElevateU team.

---

**Status**: ✅ Frontend Complete
**Last Updated**: November 20, 2025
