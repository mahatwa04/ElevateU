from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model for ElevateU.

    - Requires email addresses to be campus addresses (validation is enforced at serializer level).
    - Adds field_of_interest, bio, and campus_verified fields.
    """

    email = models.EmailField(unique=True)
    field_of_interest = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    campus_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} <{self.email}>"


class EmailVerification(models.Model):
    """Stores OTPs sent to users for email verification.
    
    - OTP expires after 10 minutes (checked at validation time).
    - Multiple OTPs can be created per user; only the latest is valid.
    - Once verified, is_verified flag is set to True.
    """

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='email_verifications'
    )
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['user', 'otp_code', 'created_at'])]
        ordering = ['-created_at']

    def __str__(self):
        status = 'VERIFIED' if self.is_verified else 'PENDING'
        return f"OTP for {self.user.email} - {status}"
