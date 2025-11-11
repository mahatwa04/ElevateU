from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer


User = get_user_model()


class RegisterAPIView(APIView):
	"""Register a new user and return JWT access & refresh tokens.

	Required fields: username, email (must be @bennett.edu.in), password, password2, field_of_interest
	"""
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			refresh = RefreshToken.for_user(user)
			data = {
				'user': UserSerializer(user).data,
				'access': str(refresh.access_token),
				'refresh': str(refresh),
			}
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginTokenObtainPairView(TokenObtainPairView):
	"""Extends the simplejwt TokenObtainPairView in case we need customization."""
	permission_classes = (permissions.AllowAny,)
