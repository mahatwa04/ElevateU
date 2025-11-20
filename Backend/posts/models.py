from django.db import models
from django.conf import settings


class Post(models.Model):
    """A simple Post model for user-generated content."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    # Use a URLField for image to avoid Pillow dependency in tests/dev
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user}"


class Achievement(models.Model):
    """Achievement model for tracking user accomplishments."""

    CATEGORY_CHOICES = [
        ("academics", "Academics"),
        ("sports", "Sports"),
        ("music", "Music"),
        ("dance", "Dance"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # author may be a user model instance; use username if available
        username = getattr(self.author, 'username', str(self.author))
        return f"{self.title} by {username}"
