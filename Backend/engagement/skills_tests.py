"""Basic tests for skills scaffolding."""
from django.test import TestCase
from django.contrib.auth import get_user_model

from .skills_models import Skill

User = get_user_model()


class SkillsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='skilluser', email='s@example.com', password='pass')

    def test_create_skill(self):
        s = Skill.objects.create(user=self.user, name='Python', category='technical', level=5)
        self.assertEqual(s.name, 'Python')
        self.assertEqual(s.level, 5)
