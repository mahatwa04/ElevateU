from django.db import models
from django.conf import settings


class Post(models.Model):
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
	# Changed from URLField to ImageField for proper file uploads
	image = models.ImageField(upload_to='posts/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	like_count = models.PositiveIntegerField(default=0)
	comment_count = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} by {self.user}"


class Like(models.Model):
	"""Track user likes on posts"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'post')

	def __str__(self):
		return f"{self.user} liked {self.post}"


class Comment(models.Model):
	"""Track comments on posts"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.user} commented on {self.post}"
