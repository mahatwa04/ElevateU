from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


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
            raise serializers.ValidationError('Registration allowed only with @bennett.edu.in email addresses')
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
