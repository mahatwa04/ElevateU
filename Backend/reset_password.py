import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Reset password for the user
user = User.objects.get(email='S25CSEU1582@bennett.edu.in')
new_password = 'Test@1234'
user.set_password(new_password)
user.save()

print(f"Password reset for {user.email}")
print(f"New password: {new_password}")
