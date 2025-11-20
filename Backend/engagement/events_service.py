"""Service helpers for events feature."""
from django.utils import timezone

from .events_models import Event, EventRegistration


class EventService:
    @staticmethod
    def is_event_live(event: Event) -> bool:
        now = timezone.now()
        return event.start_at <= now and (event.end_at is None or now <= event.end_at)

    @staticmethod
    def register_user(event: Event, user):
        obj, created = EventRegistration.objects.get_or_create(event=event, user=user)
        return obj, created
