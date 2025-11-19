from django.urls import path
from .views_extended import (
    LeaderboardAPIView,
    UserLeaderboardsAPIView,
    CalculateRankingsAPIView,
    EndorsementListCreateAPIView,
)

app_name = 'core'

urlpatterns = [
    # Leaderboard endpoints
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
    path('leaderboard/user/<int:user_id>/', UserLeaderboardsAPIView.as_view(), name='user_leaderboards'),
    
    # Ranking calculation
    path('rankings/calculate/', CalculateRankingsAPIView.as_view(), name='calculate_rankings'),
    
    # Endorsements
    path('endorsements/', EndorsementListCreateAPIView.as_view(), name='endorsements'),
]
