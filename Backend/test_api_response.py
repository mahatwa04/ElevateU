#!/usr/bin/env python
import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from users.views import ListUsersAPIView
from engagement.models import Follow

User = get_user_model()

# Create a test request
factory = RequestFactory()
request = factory.get('/api/auth/users/')
request.user = User.objects.filter(campus_verified=True).first()

# Call the API view
view = ListUsersAPIView.as_view()
response = view(request)

# Check response data
if response.data:
    first_user = response.data[0]
    print("First user in response:")
    print(f"  Username: {first_user.get('username')}")
    print(f"  ID: {first_user.get('id')}")
    print(f"  Has is_followed field: {'is_followed' in first_user}")
    if 'is_followed' in first_user:
        print(f"  is_followed value: {first_user['is_followed']}")
        print("\n✅ API response includes is_followed field!")
    else:
        print("\n❌ ERROR: is_followed field missing from API response!")
        print(f"  Available fields: {list(first_user.keys())}")
else:
    print("No data in response")
