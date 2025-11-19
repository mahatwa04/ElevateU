from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='detail'),
]
