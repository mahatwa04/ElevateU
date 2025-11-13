from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


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
from django.shortcuts import render

# Create your views here.
