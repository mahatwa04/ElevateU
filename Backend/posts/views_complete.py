from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from engagement.models import Like, Comment


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_update(self, serializer):
        # only owner can update
        if serializer.instance.user != self.request.user:
            raise PermissionError('Not allowed')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError('Not allowed')
        instance.delete()


class PostLikeAPIView(generics.CreateAPIView):
    """Like a post."""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            post.like_count += 1
            post.save()
            return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)


class PostUnlikeAPIView(generics.DestroyAPIView):
    """Unlike a post."""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            post.like_count = max(0, post.like_count - 1)
            post.save()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)


class PostCommentListAPIView(generics.ListCreateAPIView):
    """List and create comments on a post."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)
        post.comment_count += 1
        post.save()


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Detail view for comments."""
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
