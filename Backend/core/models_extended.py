from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class UserFieldRanking(models.Model):
    """Rankings for users in different fields over different time periods."""
    
    FIELD_CHOICES = [
        ('academics', 'Academics'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('dance', 'Dance'),
        ('tech', 'Tech'),
        ('arts', 'Arts'),
    ]
    
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='field_rankings')
    field = models.CharField(max_length=20, choices=FIELD_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    rank = models.IntegerField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'field', 'period')
        ordering = ['rank']
        indexes = [
            models.Index(fields=['field', 'period', '-score']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} in {self.field} ({self.period})"


class Endorsement(models.Model):
    """Skill endorsement from one user to another."""
    
    endorser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endorsements_given')
    endorsed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='endorsements_received')
    skill = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('endorser', 'endorsed_user', 'skill')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endorsed_user', 'skill']),
        ]
    
    def __str__(self):
        return f"{self.endorser.username} endorsed {self.endorsed_user.username} for {self.skill}"
