#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevateu_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

# Check Kaustubh's posts
kaustubh = User.objects.get(id=2)
print(f"Kaustubh's posts: {kaustubh.posts.all().count()}")
for post in kaustubh.posts.all():
    print(f"  - {post.id}: {post.description[:50]}")

# Check all posts
print(f"\nTotal posts in DB: {Post.objects.count()}")
for post in Post.objects.all()[:5]:
    print(f"  - User {post.user_id}: {post.description[:50]}")
