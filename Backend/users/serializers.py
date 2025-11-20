from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers

from .models import EmailVerification


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'field_of_interest',
            'bio',
            'campus_verified',
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'password2',
            'field_of_interest',
            'first_name',
            'last_name',
            'bio',
            'campus_verified',
        )
        read_only_fields = ('campus_verified',)

    def validate_email(self, value):
        """Ensure only campus emails are allowed."""
        if not value.lower().endswith('@bennett.edu.in'):
            raise serializers.ValidationError(
                'Registration allowed only with @bennett.edu.in email addresses'
            )
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered.')
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('password2', None):
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification with OTP."""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        email = attrs['email'].lower()
        otp_code = attrs['otp_code'].strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        # Check if user is already verified
        if user.campus_verified:
            raise serializers.ValidationError('Email is already verified.')

        # Get the most recent OTP for this user
        try:
            email_verification = EmailVerification.objects.filter(
                user=user,
                is_verified=False
            ).latest('created_at')
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError('No OTP found. Please register again.')

        # Check if OTP matches
        if email_verification.otp_code != otp_code:
            raise serializers.ValidationError('Invalid OTP.')

        # Check if OTP is expired (10 minutes)
        expiry_time = email_verification.created_at + timedelta(minutes=10)
        if timezone.now() > expiry_time:
            raise serializers.ValidationError('OTP has expired. Please request a new one.')

        # Store the EmailVerification object for use in the view
        attrs['email_verification'] = email_verification
        attrs['user'] = user

        return attrs
