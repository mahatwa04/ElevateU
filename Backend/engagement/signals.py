from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like, Comment


@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    if created:
        # increment the post like_count
        post = instance.post
        post.like_count = post.likes.count()
        post.save(update_fields=['like_count'])


@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    post = instance.post
    post.like_count = post.likes.count()
    post.save(update_fields=['like_count'])


@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comment_count = post.comments.count()
        post.save(update_fields=['comment_count'])


@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    post = instance.post
    post.comment_count = post.comments.count()
    post.save(update_fields=['comment_count'])
