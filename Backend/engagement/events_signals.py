"""Signals for events: notify organizer on registration (scaffold)."""
from django.dispatch import receiver
from django.db.models.signals import post_save

from .events_models import EventRegistration


@receiver(post_save, sender=EventRegistration)
def handle_registration(sender, instance, created, **kwargs):
    if created:
        # placeholder: send notification to event.organizer or enqueue task
        return
