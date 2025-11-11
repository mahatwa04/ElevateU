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
