from django.urls import path
from .views import RegisterAPIView, VerifyEmailAPIView, LoginTokenObtainPairView, GetUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth_register'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('token/', LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', GetUserAPIView.as_view(), name='get_user'),
]
