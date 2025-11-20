from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from .leaderboard_models import Leaderboard, LeaderboardUpdate
from .leaderboard_serializers import (
    LeaderboardSerializer,
    LeaderboardUpdateSerializer,
    LeaderboardListSerializer,
    UserLeaderboardStatsSerializer,
    LeaderboardTimeSeriesSerializer,
)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Leaderboard endpoints.
    
    Endpoints:
    - GET /api/leaderboard/ - List all leaderboard entries
    - GET /api/leaderboard/{id}/ - Get specific leaderboard entry
    - GET /api/leaderboard/field/{field}/ - Get leaderboard for specific field
    - GET /api/leaderboard/user/{user_id}/ - Get user's leaderboards
    - GET /api/leaderboard/weekly/ - Weekly rankings
    - GET /api/leaderboard/monthly/ - Monthly rankings
    - GET /api/leaderboard/my-stats/ - Current user's leaderboard stats
    """
    
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['score', 'rank', 'updated_at']
    ordering = ['-score']
    search_fields = ['user__username', 'field']
    
    def get_queryset(self):
        """
        Optionally filter by field if provided in query params.
        """
        queryset = Leaderboard.objects.all()
        field = self.request.query_params.get('field', None)
        if field:
            queryset = queryset.filter(field=field)
        return queryset
    
    @action(detail=False, methods=['get'])
    def field(self, request):
        """
        Get leaderboard for a specific field.
        
        Usage: GET /api/leaderboard/field/?field=sports
        """
        field = request.query_params.get('field', None)
        if not field:
            return Response(
                {'error': 'field parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leaderboards = Leaderboard.objects.filter(field=field).order_by('rank')
        serializer = LeaderboardListSerializer(leaderboards, many=True)
        
        return Response({
            'field': field,
            'count': leaderboards.count(),
            'leaderboards': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        """
        Get all leaderboards for a specific user.
        
        Usage: GET /api/leaderboard/user/?user_id=1
        """
        user_id = request.query_params.get('user_id', None)
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leaderboards = Leaderboard.objects.filter(user_id=user_id)
        serializer = LeaderboardSerializer(leaderboards, many=True)
        
        return Response({
            'user_id': user_id,
            'count': leaderboards.count(),
            'leaderboards': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """
        Get weekly leaderboard rankings.
        Includes all users sorted by weekly_score.
        
        Usage: GET /api/leaderboard/weekly/
        """
        field = request.query_params.get('field', None)
        
        queryset = Leaderboard.objects.all()
        if field:
            queryset = queryset.filter(field=field)
        
        # Sort by weekly score
        leaderboards = queryset.order_by('-weekly_score')[:50]  # Top 50
        serializer = LeaderboardTimeSeriesSerializer(leaderboards, many=True)
        
        return Response({
            'period': 'weekly',
            'field': field or 'all',
            'leaderboards': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """
        Get monthly leaderboard rankings.
        Includes all users sorted by monthly_score.
        
        Usage: GET /api/leaderboard/monthly/
        """
        field = request.query_params.get('field', None)
        
        queryset = Leaderboard.objects.all()
        if field:
            queryset = queryset.filter(field=field)
        
        # Sort by monthly score
        leaderboards = queryset.order_by('-monthly_score')[:50]  # Top 50
        serializer = LeaderboardTimeSeriesSerializer(leaderboards, many=True)
        
        return Response({
            'period': 'monthly',
            'field': field or 'all',
            'leaderboards': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def my_stats(self, request):
        """
        Get current user's leaderboard stats across all fields.
        
        Usage: GET /api/leaderboard/my-stats/
        """
        user = request.user
        leaderboards = Leaderboard.objects.filter(user=user)
        
        stats = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'field_of_interest': user.field_of_interest,
            'leaderboards': LeaderboardListSerializer(leaderboards, many=True).data,
            'total_score': sum([lb.score for lb in leaderboards]),
            'average_rank': round(sum([lb.rank for lb in leaderboards]) / max(leaderboards.count(), 1)),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def top_by_field(self, request):
        """
        Get top users for each field.
        
        Usage: GET /api/leaderboard/top-by-field/
        """
        limit = int(request.query_params.get('limit', 10))
        
        response_data = {}
        for field_code, field_name in Leaderboard.FIELD_CHOICES:
            top_users = Leaderboard.objects.filter(field=field_code).order_by('rank')[:limit]
            response_data[field_code] = LeaderboardListSerializer(top_users, many=True).data
        
        return Response(response_data)


class LeaderboardUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for LeaderboardUpdate logs.
    
    Endpoints:
    - GET /api/leaderboard-updates/ - List all updates
    - GET /api/leaderboard-updates/{id}/ - Get specific update
    - GET /api/leaderboard-updates/user/{user_id}/ - Get updates for user
    """
    
    queryset = LeaderboardUpdate.objects.all()
    serializer_class = LeaderboardUpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        """
        Get leaderboard update history for a specific user.
        
        Usage: GET /api/leaderboard-updates/user/?user_id=1
        """
        user_id = request.query_params.get('user_id', None)
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updates = LeaderboardUpdate.objects.filter(leaderboard__user_id=user_id)
        serializer = self.get_serializer(updates, many=True)
        
        return Response({
            'user_id': user_id,
            'updates': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent leaderboard updates across all users.
        
        Usage: GET /api/leaderboard-updates/recent/?limit=20
        """
        limit = int(request.query_params.get('limit', 20))
        recent_updates = LeaderboardUpdate.objects.all()[:limit]
        serializer = self.get_serializer(recent_updates, many=True)
        
        return Response({
            'count': len(recent_updates),
            'updates': serializer.data
        })
