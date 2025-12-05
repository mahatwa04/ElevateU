#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from engagement.models import Follow

# Check all follow relationships
all_follows = Follow.objects.all().values('follower_id', 'following_id')
print(f"Total Follow relationships in DB: {Follow.objects.count()}")
for follow in all_follows[:20]:
    print(f"  {follow['follower_id']} -> {follow['following_id']}")
