from django.urls import path
from .views import (
    EngagementListCreateAPIView,
    EngagementDetailAPIView,
    FollowListCreateAPIView,
    FollowDestroyAPIView,
    LikeCreateAPIView,
    CommentCreateAPIView,
)

app_name = 'engagement'

urlpatterns = [
    path('', EngagementListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', EngagementDetailAPIView.as_view(), name='detail'),
    path('follow/', FollowListCreateAPIView.as_view(), name='follow_list_create'),
    path('follow/<int:pk>/', FollowDestroyAPIView.as_view(), name='follow_detail'),
    path('like/', LikeCreateAPIView.as_view(), name='like_create'),
    path('comment/', CommentCreateAPIView.as_view(), name='comment_create'),
]
