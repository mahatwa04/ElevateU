"""
URL configuration for leaderboard endpoints.
Add to engagement/urls.py or main project urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .leaderboard_views import LeaderboardViewSet, LeaderboardUpdateViewSet

router = DefaultRouter()
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'leaderboard-updates', LeaderboardUpdateViewSet, basename='leaderboard-update')

urlpatterns = [
    path('', include(router.urls)),
]
