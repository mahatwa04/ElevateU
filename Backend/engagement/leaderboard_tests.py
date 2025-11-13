"""
Test cases for leaderboard functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post
from engagement.models import Like, Comment, Follow
from engagement.leaderboard_models import Leaderboard, LeaderboardUpdate
from engagement.leaderboard_service import LeaderboardService

User = get_user_model()


class LeaderboardModelTest(TestCase):
    """Test Leaderboard model."""
    
    def setUp(self):
        """Create test user and leaderboard."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@university.edu',
            password='testpass123',
            field_of_interest='sports'
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            field='sports',
            score=100,
            rank=5
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard is created correctly."""
        self.assertEqual(self.leaderboard.user, self.user)
        self.assertEqual(self.leaderboard.field, 'sports')
        self.assertEqual(self.leaderboard.score, 100)
    
    def test_calculate_score(self):
        """Test score calculation."""
        self.leaderboard.total_likes = 10
        self.leaderboard.total_comments = 5
        self.leaderboard.total_follows = 2
        
        expected_score = (10 * 1) + (5 * 2) + (2 * 5)  # 30
        calculated_score = self.leaderboard.calculate_score()
        
        self.assertEqual(calculated_score, expected_score)
    
    def test_unique_together(self):
        """Test that user-field combination is unique."""
        with self.assertRaises(Exception):
            Leaderboard.objects.create(
                user=self.user,
                field='sports',
                score=50,
                rank=10
            )


class LeaderboardServiceTest(TestCase):
    """Test LeaderboardService methods."""
    
    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@university.edu',
            password='testpass123',
            field_of_interest='academics'
        )
        self.post = Post.objects.create(
            user=self.user,
            title='Test Achievement',
            description='An awesome achievement',
            category='academics'
        )
    
    def test_add_like_score(self):
        """Test adding like score to leaderboard."""
        LeaderboardService.add_like_score(self.post.id, 'academics')
        
        leaderboard = Leaderboard.objects.get(user=self.user, field='academics')
        self.assertEqual(leaderboard.total_likes, 1)
        self.assertEqual(leaderboard.all_time_score, 1)  # LIKE_WEIGHT = 1
    
    def test_add_comment_score(self):
        """Test adding comment score to leaderboard."""
        LeaderboardService.add_comment_score(self.post.id, 'academics')
        
        leaderboard = Leaderboard.objects.get(user=self.user, field='academics')
        self.assertEqual(leaderboard.total_comments, 1)
        self.assertEqual(leaderboard.all_time_score, 2)  # COMMENT_WEIGHT = 2
    
    def test_add_follow_score(self):
        """Test adding follow score to leaderboard."""
        LeaderboardService.add_follow_score(self.user.id, 'academics')
        
        leaderboard = Leaderboard.objects.get(user=self.user, field='academics')
        self.assertEqual(leaderboard.total_follows, 1)
        self.assertEqual(leaderboard.all_time_score, 5)  # FOLLOW_WEIGHT = 5
    
    def test_update_rankings(self):
        """Test ranking update."""
        user2 = User.objects.create_user(
            username='user2',
            email='user2@university.edu',
            password='testpass123',
            field_of_interest='academics'
        )
        
        lb1 = Leaderboard.objects.create(user=self.user, field='academics', score=100)
        lb2 = Leaderboard.objects.create(user=user2, field='academics', score=150)
        
        LeaderboardService.update_rankings('academics')
        
        lb1.refresh_from_db()
        lb2.refresh_from_db()
        
        self.assertEqual(lb2.rank, 1)  # Higher score = rank 1
        self.assertEqual(lb1.rank, 2)
    
    def test_get_user_stats(self):
        """Test getting user stats."""
        Leaderboard.objects.create(user=self.user, field='academics', score=100, rank=5)
        Leaderboard.objects.create(user=self.user, field='sports', score=80, rank=8)
        
        stats = LeaderboardService.get_user_stats(self.user.id)
        
        self.assertEqual(stats['total_score'], 180)
        self.assertEqual(stats['field_count'], 2)
        self.assertIn('academics', stats['fields'])
        self.assertIn('sports', stats['fields'])


class LeaderboardAPITest(APITestCase):
    """Test Leaderboard API endpoints."""
    
    def setUp(self):
        """Create test user and leaderboard."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@university.edu',
            password='testpass123',
            field_of_interest='sports'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            field='sports',
            score=150,
            rank=1,
            weekly_score=50,
            monthly_score=100,
            all_time_score=150
        )
    
    def test_list_leaderboards(self):
        """Test listing leaderboards."""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_my_stats_endpoint(self):
        """Test getting current user's stats."""
        response = self.client.get('/api/leaderboard/my-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_field_leaderboard(self):
        """Test getting leaderboard for specific field."""
        response = self.client.get('/api/leaderboard/field/?field=sports')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['field'], 'sports')
    
    def test_weekly_leaderboard(self):
        """Test getting weekly leaderboard."""
        response = self.client.get('/api/leaderboard/weekly/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['period'], 'weekly')
    
    def test_monthly_leaderboard(self):
        """Test getting monthly leaderboard."""
        response = self.client.get('/api/leaderboard/monthly/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['period'], 'monthly')
    
    def test_top_by_field(self):
        """Test getting top users by field."""
        response = self.client.get('/api/leaderboard/top-by-field/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sports', response.data)
