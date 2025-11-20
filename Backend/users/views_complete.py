from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer, VerifyEmailSerializer
from .models import EmailVerification
from .email_utils import generate_otp
from django.core.mail import send_mail
from engagement.models import Follow


User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """Register a new user with @bennett.edu.in email and send OTP.

    Required fields: username, email (must be @bennett.edu.in), password, password2, field_of_interest
    
    Returns JWT tokens only after email verification.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate and send OTP
            otp = generate_otp()
            EmailVerification.objects.create(user=user, otp_code=otp)
            
            # Send OTP to email (uses console backend in dev)
            send_mail(
                subject='ElevateU Email Verification - OTP',
                message=f'Your OTP for email verification: {otp}\n\nThis OTP is valid for 10 minutes.',
                from_email='noreply@elevateu.bennett.edu.in',
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            data = {
                'user': UserSerializer(user).data,
                'message': 'OTP sent to your campus email for verification.',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(generics.CreateAPIView):
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


class LoginTokenObtainPairView(TokenObtainPairView):
    """Extends the simplejwt TokenObtainPairView in case we need customization."""
    permission_classes = (permissions.AllowAny,)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """Get and update current user profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserDetailAPIView(generics.RetrieveAPIView):
    """Get details for a specific user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()


class UserFollowersAPIView(generics.ListAPIView):
    """Get list of followers for a user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        follower_ids = Follow.objects.filter(following_id=user_id).values_list('follower_id', flat=True)
        return User.objects.filter(id__in=follower_ids)


class UserFollowingAPIView(generics.ListAPIView):
    """Get list of users that a user is following."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        following_ids = Follow.objects.filter(follower_id=user_id).values_list('following_id', flat=True)
        return User.objects.filter(id__in=following_ids)
