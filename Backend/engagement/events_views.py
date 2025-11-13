"""DRF views for events feature (scaffold)."""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .events_models import Event, EventRegistration
from .events_serializers import EventSerializer, EventRegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        # placeholder: create registration
        serializer = EventRegistrationSerializer(data={"event": event.id, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EventRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
