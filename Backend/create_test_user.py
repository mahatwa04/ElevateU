import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check existing users
print(f"Total users in database: {User.objects.count()}")
for user in User.objects.all():
    print(f"  - {user.email} ({user.username}) - verified: {user.campus_verified}")

# Create test user if none exists
if User.objects.count() == 0:
    print("\nCreating test user...")
    user = User.objects.create_user(
        username='testuser',
        email='test@bennett.edu.in',
        password='Test@1234',
        first_name='Test',
        last_name='User'
    )
    user.campus_verified = True
    user.save()
    print(f"Test user created: {user.email}")
else:
    print("\nUsers already exist in database")
