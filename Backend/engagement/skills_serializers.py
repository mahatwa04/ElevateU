"""Serializers for skills feature - small scaffolds."""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .skills_models import Skill

User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "user", "name", "category", "level", "endorsements", "created_at"]


class SkillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name", "category", "level"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        return Skill.objects.create(user=user, **validated_data)
