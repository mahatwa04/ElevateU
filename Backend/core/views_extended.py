from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models_extended import UserFieldRanking, Endorsement
from posts.models import Post
from engagement.models import Like, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFieldRankingSerializer:
    """Serializer for rankings - includes user info."""
    pass


class LeaderboardAPIView(generics.ListAPIView):
    """Get leaderboard for a specific field and time period."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        field = request.query_params.get('field', 'academics')
        period = request.query_params.get('period', 'all_time')
        limit = int(request.query_params.get('limit', 100))
        
        try:
            rankings = UserFieldRanking.objects.filter(
                field=field,
                period=period
            ).select_related('user').order_by('rank')[:limit]
            
            data = [
                {
                    'rank': r.rank,
                    'user_id': r.user.id,
                    'username': r.user.username,
                    'email': r.user.email,
                    'score': r.score,
                    'field': r.field,
                    'period': r.period,
                }
                for r in rankings
            ]
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLeaderboardsAPIView(generics.RetrieveAPIView):
    """Get all rankings for a specific user."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, user_id=None, *args, **kwargs):
        if not user_id:
            user_id = request.user.id
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        rankings = UserFieldRanking.objects.filter(user=user).values(
            'field', 'period', 'rank', 'score'
        )
        
        data = {
            'user_id': user.id,
            'username': user.username,
            'rankings': list(rankings)
        }
        
        return Response(data, status=status.HTTP_200_OK)


class CalculateRankingsAPIView(generics.CreateAPIView):
    """Calculate/recalculate all rankings."""
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        try:
            calculate_all_rankings()
            return Response(
                {'message': 'Rankings calculated successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EndorsementListCreateAPIView(generics.ListCreateAPIView):
    """List and create endorsements."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Endorsement.objects.filter(endorsed_user_id=user_id)
        return Endorsement.objects.all()
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            endorsements = Endorsement.objects.filter(endorsed_user_id=user_id).values(
                'id', 'endorser__username', 'skill', 'created_at'
            )
        else:
            endorsements = Endorsement.objects.all().values(
                'id', 'endorser__username', 'endorsed_user__username', 'skill', 'created_at'
            )
        
        return Response(list(endorsements), status=status.HTTP_200_OK)
    
    def post(self, request):
        endorsee_id = request.data.get('endorsed_user_id')
        skill = request.data.get('skill')
        
        if not endorsee_id or not skill:
            return Response(
                {'error': 'endorsed_user_id and skill required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            endorsed_user = User.objects.get(id=endorsee_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if endorsed_user == request.user:
            return Response(
                {'error': 'Cannot endorse yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        endorsement, created = Endorsement.objects.get_or_create(
            endorser=request.user,
            endorsed_user=endorsed_user,
            skill=skill
        )
        
        if created:
            return Response(
                {
                    'id': endorsement.id,
                    'endorser': endorsement.endorser.username,
                    'endorsed_user': endorsement.endorsed_user.username,
                    'skill': endorsement.skill,
                    'created_at': endorsement.created_at,
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {'error': 'Already endorsed this user for this skill'},
            status=status.HTTP_400_BAD_REQUEST
        )


def calculate_all_rankings():
    """Calculate rankings for all users in all fields."""
    fields = ['academics', 'sports', 'music', 'dance', 'tech', 'arts']
    periods = ['weekly', 'monthly', 'all_time']
    
    for field in fields:
        for period in periods:
            calculate_field_period_ranking(field, period)


def calculate_field_period_ranking(field, period):
    """Calculate ranking for a specific field and period."""
    now = timezone.now()
    
    # Determine date range based on period
    if period == 'weekly':
        start_date = now - timedelta(days=7)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:  # all_time
        start_date = None
    
    # Get all posts in the field within the period
    posts_query = Post.objects.filter(category=field)
    if start_date:
        posts_query = posts_query.filter(created_at__gte=start_date)
    
    # Calculate score for each user
    user_scores = {}
    
    for post in posts_query:
        author = post.user
        # Score calculation: likes weighted 2x, comments weighted 1x
        score = (post.like_count * 2) + (post.comment_count * 1)
        
        if author not in user_scores:
            user_scores[author] = 0
        user_scores[author] += score
    
    # Sort users by score and assign ranks
    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    
    for rank, (user, score) in enumerate(sorted_users, 1):
        UserFieldRanking.objects.update_or_create(
            user=user,
            field=field,
            period=period,
            defaults={'rank': rank, 'score': score}
        )
