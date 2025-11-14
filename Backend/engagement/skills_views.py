"""DRF view scaffolds for skills feature."""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .skills_models import Skill
from .skills_serializers import SkillSerializer, SkillCreateSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SkillCreateSerializer
        return SkillSerializer

    @action(detail=False, methods=["get"])
    def mine(self, request):
        qs = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
