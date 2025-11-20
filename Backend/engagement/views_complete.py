from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Like, Comment, Follow
from .serializers import LikeSerializer, CommentSerializer, FollowSerializer
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class LikeListCreateAPIView(generics.ListCreateAPIView):
    """List likes and create a new like."""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Like.objects.filter(post_id=post_id)
        return Like.objects.all()
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(Post, id=post_id)
        
        like, created = Like.objects.get_or_create(user=self.request.user, post=post)
        
        if created:
            post.like_count += 1
            post.save()
            return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)


class LikeDetailAPIView(generics.DestroyAPIView):
    """Delete (unlike) a like."""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError('Not allowed')
        post = instance.post
        instance.delete()
        post.like_count = max(0, post.like_count - 1)
        post.save()


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """List comments and create a new comment."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(Post, id=post_id)
        
        serializer.save(user=self.request.user, post=post)
        post.comment_count += 1
        post.save()


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Detail view for a single comment."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionError('Not allowed')
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError('Not allowed')
        post = instance.post
        instance.delete()
        post.comment_count = max(0, post.comment_count - 1)
        post.save()


class FollowListAPIView(generics.ListAPIView):
    """List all follow relationships."""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()


class FollowCreateAPIView(generics.CreateAPIView):
    """Create a follow relationship."""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following')
        
        if not following_id:
            return Response({'error': 'following id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        following_user = get_object_or_404(User, id=following_id)
        
        if following_user == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        
        if created:
            return Response(
                FollowSerializer(follow).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowAPIView(generics.DestroyAPIView):
    """Unfollow a user."""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follow.objects.all()
    
    def delete(self, request, *args, **kwargs):
        following_id = kwargs.get('user_id')
        
        try:
            follow = Follow.objects.get(follower=request.user, following_id=following_id)
            follow.delete()
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'error': 'Not following'}, status=status.HTTP_400_BAD_REQUEST)
