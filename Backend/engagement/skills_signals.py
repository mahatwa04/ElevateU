"""Signals for skills (e.g., when endorsements happen).
Currently a scaffold — real signal wiring depends on feature specifics.
"""
from django.dispatch import receiver
from django.db.models.signals import post_save

from .skills_models import Skill


@receiver(post_save, sender=Skill)
def handle_skill_saved(sender, instance, created, **kwargs):
    # placeholder: could send notifications, update search index, etc.
    if created:
        # do lightweight background work or enqueue a task
        return
