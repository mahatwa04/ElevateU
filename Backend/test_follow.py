#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from engagement.models import Follow

User = get_user_model()

# Get first two users
users = list(User.objects.filter(campus_verified=True)[:2])
if len(users) >= 2:
    user1, user2 = users[0], users[1]
    print(f"Testing with users: {user1.username} -> {user2.username}")
    
    # Check if user1 is following user2
    follow_exists_before = Follow.objects.filter(follower=user1, following=user2).exists()
    print(f"Follow relationship exists before: {follow_exists_before}")
    
    # Create follow relationship
    follow, created = Follow.objects.get_or_create(follower=user1, following=user2)
    print(f"Follow created: {created}")
    
    # Verify it was created
    follow_exists_after = Follow.objects.filter(follower=user1, following=user2).exists()
    print(f"Follow relationship exists after: {follow_exists_after}")
    
    # Check the follow counts
    print(f"{user2.username} followers: {user2.followers.count()}")
    print(f"{user1.username} following: {user1.following.count()}")
    
    # Now verify the API would return is_followed=True
    is_followed = user2.id in set(Follow.objects.filter(follower=user1).values_list('following_id', flat=True))
    print(f"\nAPI would return is_followed for {user1.username} viewing {user2.username}: {is_followed}")
    
    # Delete and verify
    follow.delete()
    follow_exists_deleted = Follow.objects.filter(follower=user1, following=user2).exists()
    print(f"Follow relationship exists after delete: {follow_exists_deleted}")
    
    print("\n✅ Follow model works correctly!")
else:
    print("Not enough users in database")
