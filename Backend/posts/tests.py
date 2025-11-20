from django.test import TestCase
from users.models import CustomUser
from .models import Post
from engagement.models import Like, Comment


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='alice', email='alice@bennett.edu.in', password='Testpass123')

    def test_create_post(self):
        p = Post.objects.create(user=self.user, title='Hello', description='World')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(p.like_count, 0)
        self.assertEqual(p.comment_count, 0)

    def test_like_and_comment_update_counts(self):
        p = Post.objects.create(user=self.user, title='Hello', description='World')
        other = CustomUser.objects.create_user(username='bob', email='bob@bennett.edu.in', password='Testpass123')
        Like.objects.create(user=other, post=p)
        p.refresh_from_db()
        self.assertEqual(p.like_count, 1)

        Comment.objects.create(user=other, post=p, text='Nice post')
        p.refresh_from_db()
        self.assertEqual(p.comment_count, 1)
from django.test import TestCase

# Create your tests here.
