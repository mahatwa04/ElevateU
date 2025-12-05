from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, PostLikeAPIView, CommentCreateAPIView

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/like/', PostLikeAPIView.as_view(), name='like'),
    path('<int:post_id>/comments/', CommentCreateAPIView.as_view(), name='create_comment'),
]
