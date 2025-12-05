#!/usr/bin/env python
import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from users.views import ListUsersAPIView
from engagement.models import Follow

User = get_user_model()

users = list(User.objects.filter(campus_verified=True)[:2])
if len(users) >= 2:
    user1, user2 = users[0], users[1]
    
    print(f"Test scenario: {user1.username} (id={user1.id}) viewing {user2.username} (id={user2.id})'s profile\n")
    
    # Clear old follows
    Follow.objects.filter(follower=user1, following=user2).delete()
    
    # Ensure follow relationship exists
    follow, created = Follow.objects.get_or_create(follower=user1, following=user2)
    print(f"Follow relationship created: {created}")
    print(f"Follow exists in DB: {Follow.objects.filter(follower=user1, following=user2).exists()}")
    
    # Create a test request from user1's perspective
    factory = RequestFactory()
    request = factory.get('/api/auth/users/')
    request.user = user1  # Properly set the user
    
    print(f"Request user: {request.user} (id={request.user.id})")
    print(f"Request user is_authenticated: {request.user.is_authenticated}")
    
    # Verify following set - MANUALLY calculate what the API should return
    following_ids = list(Follow.objects.filter(follower=user1).values_list('following_id', flat=True))
    print(f"User1's following IDs (from DB): {following_ids}")
    print(f"User2 ID: {user2.id}")
    print(f"Is {user2.id} in {following_ids}? {user2.id in following_ids}\n")
    
    # Call the API view
    view = ListUsersAPIView.as_view()
    response = view(request)
    
    # Find user2 in response
    user2_data = None
    for user_data in response.data:
        if user_data['id'] == user2.id:
            user2_data = user_data
            break
    
    if user2_data:
        print(f"Response for {user2.username}:")
        print(f"  id: {user2_data.get('id')}")
        print(f"  username: {user2_data.get('username')}")
        print(f"  is_followed: {user2_data.get('is_followed')}")
        print(f"  followers: {user2_data['profile'].get('followers')}")
        
        if user2_data.get('is_followed') == True:
            print(f"\n✅ CORRECT! is_followed=True because {user1.username} is following {user2.username}")
        else:
            print(f"\n❌ ERROR! is_followed should be True!")
            print(f"  Expected: user2.id ({user2.id}) in following_ids ({following_ids})")
            print(f"  Got: is_followed = {user2_data.get('is_followed')} (type: {type(user2_data.get('is_followed'))})")
    else:
        print(f"Could not find {user2.username} in response")
else:
    print("Not enough users")
