from django.db import models
from django.conf import settings


class Post(models.Model):
<<<<<<< HEAD
	"""A simple Post model for user-generated content.

	Fields:
	- user: FK to author
	- title: short title
	- description: body text
	- category: optional category tag
	- image: optional image upload
	- created_at / updated_at
	- like_count / comment_count: cached counters updated by signals
	"""

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
	)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	category = models.CharField(max_length=100, blank=True)
	# Use a URLField for image to avoid Pillow dependency in tests/dev
	image = models.URLField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	like_count = models.PositiveIntegerField(default=0)
	comment_count = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} by {self.user}"

<<<<<<< HEAD
=======
from django.db import models
from django.contrib.auth.models import User
=======
    """A simple Post model for user-generated content."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    # Use a URLField for image to avoid Pillow dependency in tests/dev
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user}"

>>>>>>> 808976a (fix(posts): resolve merge markers and add Achievement model)

class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ("academics", "Academics"),
        ("sports", "Sports"),
        ("music", "Music"),
        ("dance", "Dance"),
    ]

<<<<<<< HEAD
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
=======
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements'
    )
>>>>>>> 808976a (fix(posts): resolve merge markers and add Achievement model)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
<<<<<<< HEAD
# Create your models here.
>>>>>>> e329792 (feat(posts): add Achievement model + admin register + initial migration)
=======

>>>>>>> 808976a (fix(posts): resolve merge markers and add Achievement model)
