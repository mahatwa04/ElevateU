from django.urls import path
from .views import EngagementListCreateAPIView, EngagementDetailAPIView

app_name = 'engagement'

urlpatterns = [
    path('', EngagementListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', EngagementDetailAPIView.as_view(), name='detail'),
]
