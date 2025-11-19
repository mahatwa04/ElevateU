from django.urls import path
from .views_complete import (
    LikeListCreateAPIView,
    LikeDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView,
    FollowListAPIView,
    FollowCreateAPIView,
    UnfollowAPIView,
    EngagementListCreateAPIView,
    EngagementDetailAPIView,
)

app_name = 'engagement'

urlpatterns = [
    # Generic engagement endpoints
    path('', EngagementListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', EngagementDetailAPIView.as_view(), name='detail'),
    
    # Like endpoints
    path('likes/', LikeListCreateAPIView.as_view(), name='like_list_create'),
    path('likes/<int:pk>/', LikeDetailAPIView.as_view(), name='like_detail'),
    
    # Comment endpoints
    path('comments/', CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    
    # Follow endpoints
    path('follows/', FollowListAPIView.as_view(), name='follow_list'),
    path('follow/', FollowCreateAPIView.as_view(), name='follow_create'),
    path('unfollow/<int:user_id>/', UnfollowAPIView.as_view(), name='unfollow'),
]
