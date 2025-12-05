from django.urls import path
from .views import RegisterAPIView, VerifyEmailAPIView, LoginTokenObtainPairView, GetUserAPIView, ListUsersAPIView, FollowUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth_register'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('token/', LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', GetUserAPIView.as_view(), name='get_user'),
    path('users/', ListUsersAPIView.as_view(), name='list_users'),
    path('users/<int:user_id>/follow/', FollowUserAPIView.as_view(), name='follow_user'),
]
