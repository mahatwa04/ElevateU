import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Verify the user
user = User.objects.get(email='S25CSEU1582@bennett.edu.in')
user.campus_verified = True
user.save()

print(f"User {user.email} is now verified!")
print(f"Username: {user.username}")
print(f"Campus Verified: {user.campus_verified}")
print("\nYou can now try logging in with this account.")
print("Note: You'll need to know the password for this account.")
print("\nOr use the demo account:")
print("Email: demo@bennett.edu.in")
print("Password: Demo@1234")
