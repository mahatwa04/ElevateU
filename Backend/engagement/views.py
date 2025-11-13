from rest_framework import generics, permissions
from django.contrib.contenttypes.models import ContentType
from .models import Engagement
from .serializers import EngagementSerializer


class EngagementListCreateAPIView(generics.ListCreateAPIView):
    """List engagements and allow authenticated users to create engagements.

    Query params (optional):
    - content_type (model name, e.g. 'customuser')
    - object_id (integer)
    """

    serializer_class = EngagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Engagement.objects.all()
        ct = self.request.query_params.get('content_type')
        obj_id = self.request.query_params.get('object_id')
        if ct and obj_id:
            try:
                content_type = ContentType.objects.get(model=ct)
                qs = qs.filter(content_type=content_type, object_id=obj_id)
            except ContentType.DoesNotExist:
                return Engagement.objects.none()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EngagementDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = EngagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Engagement.objects.all()

    def delete(self, request, *args, **kwargs):
        # Only the owner may delete their engagement
        obj = self.get_object()
        if obj.user != request.user:
            return generics.Response({'detail': 'Not allowed'}, status=403)
        return super().delete(request, *args, **kwargs)
