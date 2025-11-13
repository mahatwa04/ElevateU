from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Engagement(models.Model):
    """Generic engagement record that can attach to any model via GenericForeignKey.

    Fields:
    - user: FK to the actor (AUTH_USER_MODEL)
    - content_object: generic foreign key to the target (post, profile, etc.)
    - type: one of 'like', 'comment', 'reaction'
    - comment: optional text for comments
    - reaction: optional short label for reaction (like 'heart')
    - created_at: timestamp
    """

    LIKE = 'like'
    COMMENT = 'comment'
    REACTION = 'reaction'

    TYPE_CHOICES = [
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (REACTION, 'Reaction'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='engagements',
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    reaction = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.user} {self.type} -> {self.content_type}#{self.object_id}"


class Like(models.Model):
    """Like on a Post by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} likes {self.post_id}"


class Comment(models.Model):
    """Comment on a Post by a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user} on {self.post_id}"


class Follow(models.Model):
    """User-to-user follow relationship."""

    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} -> {self.following}"
