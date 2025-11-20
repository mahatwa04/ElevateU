from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, VerifyEmailSerializer
from .models import EmailVerification
from .email_utils import generate_otp


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


class LoginTokenObtainPairView(TokenObtainPairView):
    """Extends the simplejwt TokenObtainPairView in case we need customization."""
    permission_classes = (permissions.AllowAny,)

