"""
Django signals for leaderboard updates.
Triggered when likes, comments, or follows are created.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like, Comment, Follow
from .leaderboard_service import LeaderboardService
from posts.models import Post


@receiver(post_save, sender=Like)
def update_leaderboard_on_like(sender, instance, created, **kwargs):
    """
    Update leaderboard when a like is created.
    """
    if created:
        try:
            post = instance.post
            field = post.category if post.category else 'other'
            LeaderboardService.add_like_score(post.id, field)
        except Exception as e:
            print(f"Error updating leaderboard on like: {str(e)}")


@receiver(post_delete, sender=Like)
def update_leaderboard_on_like_delete(sender, instance, **kwargs):
    """
    Update leaderboard when a like is deleted (deduct points).
    """
    try:
        from .leaderboard_models import Leaderboard
        
        post = instance.post
        field = post.category if post.category else 'other'
        
        leaderboard = Leaderboard.objects.get(user=post.user, field=field)
        leaderboard.total_likes = max(0, leaderboard.total_likes - 1)
        leaderboard.all_time_score = max(0, leaderboard.all_time_score - LeaderboardService.LIKE_WEIGHT)
        leaderboard.weekly_score = max(0, leaderboard.weekly_score - LeaderboardService.LIKE_WEIGHT)
        leaderboard.monthly_score = max(0, leaderboard.monthly_score - LeaderboardService.LIKE_WEIGHT)
        leaderboard.score = leaderboard.calculate_score()
        leaderboard.save()
        
        LeaderboardService.update_rankings(field)
    except Exception as e:
        print(f"Error updating leaderboard on like delete: {str(e)}")


@receiver(post_save, sender=Comment)
def update_leaderboard_on_comment(sender, instance, created, **kwargs):
    """
    Update leaderboard when a comment is created.
    """
    if created:
        try:
            post = instance.post
            field = post.category if post.category else 'other'
            LeaderboardService.add_comment_score(post.id, field)
        except Exception as e:
            print(f"Error updating leaderboard on comment: {str(e)}")


@receiver(post_delete, sender=Comment)
def update_leaderboard_on_comment_delete(sender, instance, **kwargs):
    """
    Update leaderboard when a comment is deleted (deduct points).
    """
    try:
        from .leaderboard_models import Leaderboard
        
        post = instance.post
        field = post.category if post.category else 'other'
        
        leaderboard = Leaderboard.objects.get(user=post.user, field=field)
        leaderboard.total_comments = max(0, leaderboard.total_comments - 1)
        leaderboard.all_time_score = max(0, leaderboard.all_time_score - LeaderboardService.COMMENT_WEIGHT)
        leaderboard.weekly_score = max(0, leaderboard.weekly_score - LeaderboardService.COMMENT_WEIGHT)
        leaderboard.monthly_score = max(0, leaderboard.monthly_score - LeaderboardService.COMMENT_WEIGHT)
        leaderboard.score = leaderboard.calculate_score()
        leaderboard.save()
        
        LeaderboardService.update_rankings(field)
    except Exception as e:
        print(f"Error updating leaderboard on comment delete: {str(e)}")


@receiver(post_save, sender=Follow)
def update_leaderboard_on_follow(sender, instance, created, **kwargs):
    """
    Update leaderboard when a user is followed.
    """
    if created:
        try:
            # Get the user's primary field
            user = instance.following
            field = user.field_of_interest if user.field_of_interest else 'other'
            LeaderboardService.add_follow_score(user.id, field)
        except Exception as e:
            print(f"Error updating leaderboard on follow: {str(e)}")


@receiver(post_delete, sender=Follow)
def update_leaderboard_on_follow_delete(sender, instance, **kwargs):
    """
    Update leaderboard when a follow is deleted (deduct points).
    """
    try:
        from .leaderboard_models import Leaderboard
        
        user = instance.following
        field = user.field_of_interest if user.field_of_interest else 'other'
        
        leaderboard = Leaderboard.objects.get(user=user, field=field)
        leaderboard.total_follows = max(0, leaderboard.total_follows - 1)
        leaderboard.all_time_score = max(0, leaderboard.all_time_score - LeaderboardService.FOLLOW_WEIGHT)
        leaderboard.weekly_score = max(0, leaderboard.weekly_score - LeaderboardService.FOLLOW_WEIGHT)
        leaderboard.monthly_score = max(0, leaderboard.monthly_score - LeaderboardService.FOLLOW_WEIGHT)
        leaderboard.score = leaderboard.calculate_score()
        leaderboard.save()
        
        LeaderboardService.update_rankings(field)
    except Exception as e:
        print(f"Error updating leaderboard on follow delete: {str(e)}")
