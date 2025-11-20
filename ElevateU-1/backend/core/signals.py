from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a user profile or perform any action needed when a user is created
        pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the user profile or perform any action needed when a user is updated
    pass