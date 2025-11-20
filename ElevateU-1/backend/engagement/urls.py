from django.urls import path
from . import views

urlpatterns = [
    path('likes/', views.LikeListCreateView.as_view(), name='like-list-create'),
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('follow/', views.FollowListCreateView.as_view(), name='follow-list-create'),
]