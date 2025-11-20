"""Scaffold models for skills feature.
Minimal, safe definitions to be expanded later.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SkillCategory(models.TextChoices):
    TECHNICAL = "technical", "Technical"
    SOFT = "soft", "Soft"
    CREATIVE = "creative", "Creative"


class Skill(models.Model):
    """A skill that users can have and be ranked on."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=32, choices=SkillCategory.choices, default=SkillCategory.TECHNICAL)
    level = models.PositiveSmallIntegerField(default=1)  # 1..10
    endorsements = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "name")
        indexes = [models.Index(fields=["name"]), models.Index(fields=["user", "name"]) ]

    def __str__(self):
        return f"{self.user} - {self.name} (lvl {self.level})"
