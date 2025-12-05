#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
# Get Kaustubh (id=2)
kaustubh = User.objects.get(id=2)
print(f"Kaustubh followers count: {kaustubh.followers.count()}")
print(f"Kaustubh followers: {list(kaustubh.followers.all().values_list('username', flat=True))}")
