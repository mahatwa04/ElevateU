"""
Leaderboard service functions for score calculation and ranking updates.
"""

from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from .leaderboard_models import Leaderboard, LeaderboardUpdate
from posts.models import Post
from engagement.models import Like, Comment, Follow


class LeaderboardService:
    """
    Service class for managing leaderboard scores and rankings.
    """
    
    # Score weights
    LIKE_WEIGHT = 1
    COMMENT_WEIGHT = 2
    FOLLOW_WEIGHT = 5
    
    @staticmethod
    def add_like_score(post_id, field):
        """
        Update leaderboard when a post receives a like.
        
        Args:
            post_id: ID of the post that was liked
            field: Field/category of the post
        """
        try:
            post = Post.objects.get(id=post_id)
            leaderboard, _ = Leaderboard.objects.get_or_create(
                user=post.user,
                field=field
            )
            
            previous_rank = leaderboard.rank
            
            # Update counts
            leaderboard.total_likes += 1
            leaderboard.all_time_score += LeaderboardService.LIKE_WEIGHT
            leaderboard.weekly_score += LeaderboardService.LIKE_WEIGHT
            leaderboard.monthly_score += LeaderboardService.LIKE_WEIGHT
            leaderboard.score = leaderboard.calculate_score()
            
            leaderboard.save()
            
            # Update rank
            new_rank = LeaderboardService.update_rankings(field)
            new_rank = leaderboard.rank
            
            # Log the update
            LeaderboardUpdate.objects.create(
                leaderboard=leaderboard,
                previous_rank=previous_rank,
                new_rank=new_rank,
                score_change=LeaderboardService.LIKE_WEIGHT,
                reason='like',
                post_id=post_id
            )
            
        except Post.DoesNotExist:
            pass
    
    @staticmethod
    def add_comment_score(post_id, field):
        """
        Update leaderboard when a post receives a comment.
        
        Args:
            post_id: ID of the post that was commented on
            field: Field/category of the post
        """
        try:
            post = Post.objects.get(id=post_id)
            leaderboard, _ = Leaderboard.objects.get_or_create(
                user=post.user,
                field=field
            )
            
            previous_rank = leaderboard.rank
            
            # Update counts
            leaderboard.total_comments += 1
            leaderboard.all_time_score += LeaderboardService.COMMENT_WEIGHT
            leaderboard.weekly_score += LeaderboardService.COMMENT_WEIGHT
            leaderboard.monthly_score += LeaderboardService.COMMENT_WEIGHT
            leaderboard.score = leaderboard.calculate_score()
            
            leaderboard.save()
            
            # Update rank
            new_rank = LeaderboardService.update_rankings(field)
            new_rank = leaderboard.rank
            
            # Log the update
            LeaderboardUpdate.objects.create(
                leaderboard=leaderboard,
                previous_rank=previous_rank,
                new_rank=new_rank,
                score_change=LeaderboardService.COMMENT_WEIGHT,
                reason='comment',
                post_id=post_id
            )
            
        except Post.DoesNotExist:
            pass
    
    @staticmethod
    def add_follow_score(user_id, field):
        """
        Update leaderboard when a user gets followed.
        
        Args:
            user_id: ID of the user being followed
            field: Field/category of the user
        """
        try:
            leaderboard, _ = Leaderboard.objects.get_or_create(
                user_id=user_id,
                field=field
            )
            
            previous_rank = leaderboard.rank
            
            # Update counts
            leaderboard.total_follows += 1
            leaderboard.all_time_score += LeaderboardService.FOLLOW_WEIGHT
            leaderboard.weekly_score += LeaderboardService.FOLLOW_WEIGHT
            leaderboard.monthly_score += LeaderboardService.FOLLOW_WEIGHT
            leaderboard.score = leaderboard.calculate_score()
            
            leaderboard.save()
            
            # Update rank
            new_rank = LeaderboardService.update_rankings(field)
            new_rank = leaderboard.rank
            
            # Log the update
            LeaderboardUpdate.objects.create(
                leaderboard=leaderboard,
                previous_rank=previous_rank,
                new_rank=new_rank,
                score_change=LeaderboardService.FOLLOW_WEIGHT,
                reason='follow'
            )
            
        except Exception as e:
            print(f"Error updating follow score: {str(e)}")
    
    @staticmethod
    def update_rankings(field):
        """
        Update rankings for a specific field.
        Assigns rank based on score (1 = highest score).
        
        Args:
            field: Field/category to update rankings for
        
        Returns:
            Number of leaderboards updated
        """
        leaderboards = Leaderboard.objects.filter(field=field).order_by('-score')
        
        updated_count = 0
        for rank, leaderboard in enumerate(leaderboards, start=1):
            if leaderboard.rank != rank:
                leaderboard.rank = rank
                leaderboard.save(update_fields=['rank'])
                updated_count += 1
        
        return updated_count
    
    @staticmethod
    def update_all_rankings():
        """
        Update rankings for all fields.
        Should be called periodically (via Celery task).
        """
        for field_code, _ in Leaderboard.FIELD_CHOICES:
            LeaderboardService.update_rankings(field_code)
    
    @staticmethod
    def reset_weekly_scores():
        """
        Reset all weekly scores.
        Should be called once per week (via Celery task).
        """
        now = timezone.now()
        reset_count = Leaderboard.objects.filter(
            weekly_reset_at__lt=now - timedelta(days=7)
        ).update(weekly_score=0, weekly_reset_at=now)
        
        return reset_count
    
    @staticmethod
    def reset_monthly_scores():
        """
        Reset all monthly scores.
        Should be called once per month (via Celery task).
        """
        now = timezone.now()
        reset_count = Leaderboard.objects.filter(
            monthly_reset_at__lt=now - timedelta(days=30)
        ).update(monthly_score=0, monthly_reset_at=now)
        
        return reset_count
    
    @staticmethod
    def get_user_stats(user_id):
        """
        Get comprehensive stats for a user across all fields.
        
        Args:
            user_id: ID of the user
        
        Returns:
            Dictionary with user stats
        """
        leaderboards = Leaderboard.objects.filter(user_id=user_id)
        
        return {
            'total_score': sum([lb.score for lb in leaderboards]),
            'avg_rank': round(sum([lb.rank for lb in leaderboards]) / max(leaderboards.count(), 1)),
            'field_count': leaderboards.count(),
            'fields': {
                lb.field: {
                    'score': lb.score,
                    'rank': lb.rank,
                    'likes': lb.total_likes,
                    'comments': lb.total_comments,
                    'follows': lb.total_follows
                }
                for lb in leaderboards
            }
        }
    
    @staticmethod
    def get_field_leaders(field, limit=10):
        """
        Get top users in a specific field.
        
        Args:
            field: Field/category
            limit: Number of top users to return
        
        Returns:
            QuerySet of top Leaderboard entries
        """
        return Leaderboard.objects.filter(field=field).order_by('rank')[:limit]
    
    @staticmethod
    def get_weekly_leaders(field=None, limit=10):
        """
        Get top users by weekly score.
        
        Args:
            field: Optional field filter
            limit: Number of top users to return
        
        Returns:
            QuerySet of Leaderboard entries
        """
        queryset = Leaderboard.objects.all()
        if field:
            queryset = queryset.filter(field=field)
        
        return queryset.order_by('-weekly_score')[:limit]
    
    @staticmethod
    def get_monthly_leaders(field=None, limit=10):
        """
        Get top users by monthly score.
        
        Args:
            field: Optional field filter
            limit: Number of top users to return
        
        Returns:
            QuerySet of Leaderboard entries
        """
        queryset = Leaderboard.objects.all()
        if field:
            queryset = queryset.filter(field=field)
        
        return queryset.order_by('-monthly_score')[:limit]
