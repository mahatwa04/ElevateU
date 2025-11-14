"""Serializers for events feature."""
from rest_framework import serializers

from .events_models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "description", "organizer", "start_at", "end_at", "location"]


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ["id", "event", "user", "registered_at"]
