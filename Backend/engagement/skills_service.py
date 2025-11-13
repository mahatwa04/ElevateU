"""Service layer for skills feature - scoring and simple helpers.
This file intentionally minimal: add more logic as feature requirements evolve.
"""
from django.db import transaction
from django.db import models

from .skills_models import Skill


class SkillService:
    @staticmethod
    def endorse_skill(skill: Skill, count: int = 1):
        """Increment endorsements atomically."""
        with transaction.atomic():
            skill.endorsements = models.F('endorsements') + count
            skill.save(update_fields=['endorsements'])
            # refresh from db to get integer value
            skill.refresh_from_db()
        return skill

    @staticmethod
    def set_level(skill: Skill, level: int):
        if not 1 <= level <= 10:
            raise ValueError("level must be between 1 and 10")
        skill.level = level
        skill.save(update_fields=["level"])
        return skill
