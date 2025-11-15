from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from .models import Engagement, Follow


class EngagementAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='alice', email='alice@bennett.edu.in', password='Testpass123')
        self.other = CustomUser.objects.create_user(username='bob', email='bob@bennett.edu.in', password='Testpass123')
        self.list_url = reverse('engagement:list_create')

    def test_create_like_engagement(self):
        self.client.force_authenticate(self.user)
        ct = ContentType.objects.get_for_model(self.other)
        payload = {
            'content_type': ct.model,
            'object_id': self.other.id,
            'type': Engagement.LIKE,
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Engagement.objects.count(), 1)

    def test_create_comment_requires_text(self):
        self.client.force_authenticate(self.user)
        ct = ContentType.objects.get_for_model(self.other)
        payload = {
            'content_type': ct.model,
            'object_id': self.other.id,
            'type': Engagement.COMMENT,
        }
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('comment', resp.data)

    def test_list_engagements_for_object(self):
        # create a like and a comment
        Engagement.objects.create(user=self.user, content_object=self.other, type=Engagement.LIKE)
        Engagement.objects.create(user=self.other, content_object=self.user, type=Engagement.COMMENT, comment='Nice')

        ct = ContentType.objects.get_for_model(self.other)
        resp = self.client.get(self.list_url, {'content_type': ct.model, 'object_id': self.other.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_follow_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('engagement:follow_list_create')
        payload = {'following': self.other.id}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

    def test_cannot_follow_self(self):
        self.client.force_authenticate(self.user)
        url = reverse('engagement:follow_list_create')
        payload = {'following': self.user.id}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow(self):
        f = Follow.objects.create(follower=self.user, following=self.other)
        self.client.force_authenticate(self.user)
        url = reverse('engagement:follow_detail', kwargs={'pk': f.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)

    def test_list_followers(self):
        Follow.objects.create(follower=self.user, following=self.other)
        url = reverse('engagement:follow_list_create')
        resp = self.client.get(url, {'user': self.other.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
