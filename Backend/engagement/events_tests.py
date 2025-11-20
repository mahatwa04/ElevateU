"""Basic tests for events scaffolding."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from .events_models import Event, EventRegistration

User = get_user_model()


class EventsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='eventuser', email='e@example.com', password='pass')

    def test_create_event_and_registration(self):
        start = timezone.now()
        ev = Event.objects.create(title='Test', organizer=self.user, start_at=start)
        reg = EventRegistration.objects.create(event=ev, user=self.user)
        self.assertEqual(reg.event, ev)
        self.assertEqual(reg.user, self.user)
