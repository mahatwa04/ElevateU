from rest_framework import serializers
from django.contrib.auth import get_user_model
from .leaderboard_models import Leaderboard, LeaderboardUpdate

User = get_user_model()


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user_id', 'user_username', 'user_email',
            'field', 'score', 'rank',
            'weekly_score', 'monthly_score', 'all_time_score',
            'total_likes', 'total_comments', 'total_follows',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'score', 'rank', 'weekly_score', 'monthly_score',
            'all_time_score', 'total_likes', 'total_comments',
            'total_follows', 'created_at', 'updated_at'
        ]


class LeaderboardUpdateSerializer(serializers.ModelSerializer):
    """Serializer for LeaderboardUpdate model."""
    
    leaderboard_field = serializers.CharField(source='leaderboard.field', read_only=True)
    leaderboard_user = serializers.CharField(source='leaderboard.user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = LeaderboardUpdate
        fields = [
            'id', 'leaderboard_field', 'leaderboard_user',
            'previous_rank', 'new_rank', 'score_change', 'reason',
            'post_title', 'created_at'
        ]
        read_only_fields = ['created_at']


class LeaderboardListSerializer(serializers.ModelSerializer):
    """Serializer for leaderboard list view - simpler version."""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'username', 'field', 'score', 'rank', 'total_likes', 'total_comments', 'total_follows']


class UserLeaderboardStatsSerializer(serializers.Serializer):
    """Serializer for user leaderboard stats across all fields."""
    
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    field_of_interest = serializers.CharField(read_only=True)
    leaderboards = LeaderboardListSerializer(many=True, read_only=True)
    total_score = serializers.SerializerMethodField()
    total_rank = serializers.SerializerMethodField()
    
    def get_total_score(self, obj):
        """Calculate total score across all fields."""
        return sum([lb.score for lb in obj.leaderboards.all()])
    
    def get_total_rank(self, obj):
        """Calculate average rank across all fields."""
        leaderboards = obj.leaderboards.all()
        if leaderboards.exists():
            return round(sum([lb.rank for lb in leaderboards]) / leaderboards.count())
        return 0


class LeaderboardTimeSeriesSerializer(serializers.ModelSerializer):
    """Serializer for time-based leaderboard views (weekly, monthly, all-time)."""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'username', 'field', 'rank',
            'weekly_score', 'monthly_score', 'all_time_score'
        ]
