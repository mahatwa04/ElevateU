from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def get_queryset(self):
        """Filter posts by user if user query parameter is provided"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

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


class PostLikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def post(self, request, pk):
        """Like or unlike a post"""
        post = self.get_object()
        user = request.user
        
        # Check if user already liked
        like = Like.objects.filter(user=user, post=post).first()
        
        if like:
            # Unlike
            like.delete()
            post.like_count = max(0, post.like_count - 1)
            post.save()
            return Response({'liked': False, 'like_count': post.like_count}, status=status.HTTP_200_OK)
        else:
            # Like
            Like.objects.create(user=user, post=post)
            post.like_count += 1
            post.save()
            return Response({'liked': True, 'like_count': post.like_count}, status=status.HTTP_200_OK)


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        text = request.data.get('text')
        
        if not text or not text.strip():
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                text=text.strip()
            )
            post.comment_count = post.post_comments.count()
            post.save()
            return Response(CommentSerializer(comment, context={'request': request}).data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
