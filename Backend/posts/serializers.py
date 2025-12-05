from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_profile_photo', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'user_profile_photo', 'created_at')

    def get_user(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username

    def get_user_profile_photo(self, obj):
        return obj.user.profile_photo if obj.user.profile_photo else None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_profile_photo = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    comments = CommentSerializer(source='post_comments', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'user_profile_photo', 'title', 'description', 'category', 'image', 'image_url', 'created_at', 'updated_at', 'like_count', 'comment_count', 'comments')
        read_only_fields = ('id', 'user', 'user_profile_photo', 'created_at', 'updated_at', 'like_count', 'comment_count', 'comments')

    def get_user(self, obj):
        """Return user's full name if available, otherwise username"""
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username

    def get_user_profile_photo(self, obj):
        """Return user's profile photo URL if available"""
        return obj.user.profile_photo if obj.user.profile_photo else None

    def get_image_url(self, obj):
        """Return full URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
