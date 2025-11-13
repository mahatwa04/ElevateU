from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Leaderboard(models.Model):
    """
    Field-based leaderboard rankings.
    Stores ranking scores for users in different fields.
    
    Fields:
    - user: FK to CustomUser
    - field: Field of achievement (academics, sports, music, dance, etc.)
    - score: Total engagement score (likes + comments*2 + follows*5)
    - rank: Current rank in the field
    - weekly_score: Score for current week
    - monthly_score: Score for current month
    - all_time_score: Total all-time score
    - updated_at: Last update timestamp
    """
    
    FIELD_CHOICES = [
        ('academics', 'Academics'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('dance', 'Dance'),
        ('art', 'Art'),
        ('technology', 'Technology'),
        ('leadership', 'Leadership'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leaderboards'
    )
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    
    # Ranking scores
    score = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    
    # Time-based scores
    weekly_score = models.PositiveIntegerField(default=0)
    monthly_score = models.PositiveIntegerField(default=0)
    all_time_score = models.PositiveIntegerField(default=0)
    
    # Engagement counts
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_follows = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weekly_reset_at = models.DateTimeField(null=True, blank=True)
    monthly_reset_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'field')
        ordering = ['-score']
        indexes = [
            models.Index(fields=['field', '-score']),
            models.Index(fields=['user', 'field']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.field} (Rank: {self.rank})"
    
    def calculate_score(self):
        """Calculate leaderboard score based on engagement."""
        # Score formula: likes (1 pt) + comments (2 pts) + follows (5 pts)
        return (self.total_likes * 1) + (self.total_comments * 2) + (self.total_follows * 5)
    
    def reset_weekly_if_needed(self):
        """Reset weekly score if a week has passed."""
        now = timezone.now()
        if self.weekly_reset_at is None or (now - self.weekly_reset_at) >= timedelta(days=7):
            self.weekly_score = 0
            self.weekly_reset_at = now
            self.save()
    
    def reset_monthly_if_needed(self):
        """Reset monthly score if a month has passed."""
        now = timezone.now()
        if self.monthly_reset_at is None or (now - self.monthly_reset_at) >= timedelta(days=30):
            self.monthly_score = 0
            self.monthly_reset_at = now
            self.save()


class LeaderboardUpdate(models.Model):
    """
    Log of leaderboard score updates.
    Used for tracking changes in rankings.
    
    Fields:
    - leaderboard: FK to Leaderboard
    - previous_rank: Previous rank before update
    - new_rank: New rank after update
    - score_change: Points added/removed
    - reason: Why the score changed (like, comment, follow, etc.)
    - post_id: Related post (optional)
    - created_at: Timestamp
    """
    
    REASON_CHOICES = [
        ('like', 'Like on Post'),
        ('comment', 'Comment on Post'),
        ('follow', 'User Followed'),
        ('manual', 'Manual Adjustment'),
    ]
    
    leaderboard = models.ForeignKey(
        Leaderboard,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    previous_rank = models.PositiveIntegerField(null=True, blank=True)
    new_rank = models.PositiveIntegerField(null=True, blank=True)
    score_change = models.IntegerField(default=0)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leaderboard_updates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['leaderboard', '-created_at']),
        ]
    
    def __str__(self):
        return f"Rank {self.previous_rank} → {self.new_rank} for {self.leaderboard.user}"
