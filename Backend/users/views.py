from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings

from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, VerifyEmailSerializer
from .models import EmailVerification
from .email_utils import generate_otp
from engagement.models import Follow


User = get_user_model()


class RegisterAPIView(APIView):
    """Register a new user with @bennett.edu.in email and send OTP.

    Required fields: username, email (must be @bennett.edu.in), password, password2, field_of_interest
    
    Returns JWT tokens only after email verification.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Mark user as verified immediately (no OTP required)
            user.campus_verified = True
            user.save()
            
            # Issue JWT tokens directly
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Registration successful! You are now logged in.',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    """Verify email with OTP and return JWT tokens.
    
    Requires: email, otp_code (6-digit numeric).
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            email_verification = serializer.validated_data['email_verification']
            
            # Mark as verified
            email_verification.is_verified = True
            email_verification.save()
            
            # Mark user as campus verified
            user.campus_verified = True
            user.save()
            
            # Issue JWT tokens
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Email verified successfully!',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenObtainPairView(APIView):
    """Login with email and password, returns JWT tokens."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find user by email (case-insensitive)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if password is correct
        if not user.check_password(password):
            return Response(
                {'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if email is verified
        if not user.campus_verified:
            return Response(
                {'detail': 'Email not verified. Please verify your email first.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class GetUserAPIView(APIView):
    """Get current user profile."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        
        # Calculate achievements (user's posts count)
        achievements = 0
        if hasattr(user, 'posts'):
            achievements = user.posts.all().count()
        
        # Get total likes received
        total_likes = 0
        if hasattr(user, 'posts'):
            for post in user.posts.all():
                total_likes += post.like_count
        
        # Get follower/following counts from Follow relationships
        followers = user.followers.count()
        following = user.following.count()
        
        user_data = UserSerializer(user).data
        user_data['achievements'] = achievements
        user_data['profile'] = {
            'followers': followers,
            'following': following,
            'likes': total_likes,
        }
        return Response(user_data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Update user profile (first_name, last_name, field_of_interest, bio)."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersAPIView(APIView):
    """List all users for leaderboard."""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        users = User.objects.filter(campus_verified=True)
        user_data = []
        
        # Get current user's following list if authenticated
        current_user_following_ids = set()
        if request.user.is_authenticated:
            current_user_following_ids = set(
                Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
            )
        
        for user in users:
            # Get user's posts count (only verified)
            achievements = 0
            if hasattr(user, 'posts'):
                achievements = user.posts.all().count()
            
            # Get total likes received on all user's posts
            total_likes = 0
            if hasattr(user, 'posts'):
                for post in user.posts.all():
                    total_likes += post.like_count
            
            # Check if current user is following this user
            is_followed = user.id in current_user_following_ids
            
            # Get follower/following counts from Follow relationships
            followers_count = user.followers.count()
            following_count = user.following.count()
            
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                'field_of_interest': user.field_of_interest,
                'bio': user.bio,
                'profile_photo': user.profile_photo,
                'achievements': achievements,
                'verified_achievements': achievements,
                'is_followed': is_followed,
                'profile': {
                    'department': user.profile.department if hasattr(user, 'profile') else user.field_of_interest,
                    'bio': user.profile.bio if hasattr(user, 'profile') else user.bio,
                    'followers': followers_count,
                    'following': following_count,
                    'likes': total_likes,
                },
            })
        return Response(user_data, status=status.HTTP_200_OK)


class FollowUserAPIView(APIView):
    """Follow/Unfollow a user."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        """Follow a user."""
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user.id == user_id:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )
        
        if created:
            return Response(
                {'detail': 'You are now following this user.'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'detail': 'You are already following this user.'},
                status=status.HTTP_200_OK
            )

    def delete(self, request, user_id):
        """Unfollow a user."""
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            follow = Follow.objects.get(
                follower=request.user,
                following=target_user
            )
            follow.delete()
            return Response(
                {'detail': 'You have unfollowed this user.'},
                status=status.HTTP_200_OK
            )
        except Follow.DoesNotExist:
            return Response(
                {'detail': 'You are not following this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
