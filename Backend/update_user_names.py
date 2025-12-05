import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Update the test user with proper first and last names
user = User.objects.get(email='S25CSEU1582@bennett.edu.in')
user.first_name = 'Test'
user.last_name = 'User'
user.save()

print(f"Updated user: {user.username}")
print(f"First Name: {user.first_name}")
print(f"Last Name: {user.last_name}")
print(f"Email: {user.email}")
