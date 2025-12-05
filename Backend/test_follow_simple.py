#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from engagement.models import Follow

User = get_user_model()
user1 = User.objects.get(id=1)
user2 = User.objects.get(id=2)

print(f"Testing: {user1.username} (id={user1.id}) following {user2.username} (id={user2.id})")

# Create follow
follow, created = Follow.objects.get_or_create(follower=user1, following=user2)
print(f"Created: {created}")

# Method 1: Set
following_set = set(Follow.objects.filter(follower=user1).values_list('following_id', flat=True))
print(f"Method 1 (set): {user2.id} in {following_set} = {user2.id in following_set}")

# Method 2: List
following_list = list(Follow.objects.filter(follower=user1).values_list('following_id', flat=True))
print(f"Method 2 (list): {user2.id} in {following_list} = {user2.id in following_list}")

# Method 3: QuerySet
following_qs = Follow.objects.filter(follower=user1, following=user2).exists()
print(f"Method 3 (exists): {following_qs}")

# Check raw
follow_obj = Follow.objects.get(follower=user1, following=user2)
print(f"Follow object: {follow_obj}")
print(f"Follow.following_id: {follow_obj.following_id}")
print(f"User2.id: {user2.id}")
print(f"Are they equal? {follow_obj.following_id == user2.id}")
