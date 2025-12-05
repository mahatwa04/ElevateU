import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create a new test user with known password
email = 'demo@bennett.edu.in'
password = 'Demo@1234'

# Delete if exists
User.objects.filter(email=email).delete()

# Create new user
user = User.objects.create_user(
    username='demouser',
    email=email,
    password=password,
    first_name='Demo',
    last_name='User'
)
user.campus_verified = True
user.save()

print(f"Test user created successfully!")
print(f"Email: {email}")
print(f"Password: {password}")
