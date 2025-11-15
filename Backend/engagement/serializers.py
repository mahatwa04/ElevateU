from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Engagement
from .models import Like, Comment, Follow
from posts.models import Post
from users.models import CustomUser


class EngagementSerializer(serializers.ModelSerializer):
    # allow passing model name for convenience (e.g. ?content_type=customuser)
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all(),
    )

    class Meta:
        model = Engagement
        fields = ('id', 'user', 'content_type', 'object_id', 'type', 'comment', 'reaction', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def validate(self, attrs):
        """Ensure required fields for each engagement type."""
        engagement_type = attrs.get('type')
        comment = attrs.get('comment')
        reaction = attrs.get('reaction')

        if engagement_type == Engagement.COMMENT and not comment:
            raise serializers.ValidationError({'comment': 'Comment text is required for comment engagements.'})

        if engagement_type == Engagement.REACTION and not reaction:
            raise serializers.ValidationError({'reaction': 'Reaction label is required for reaction engagements.'})

        return attrs


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('id', 'follower', 'created_at')

    def validate(self, attrs):
        request = self.context.get('request')
        following = attrs.get('following')
        if request and hasattr(request, 'user') and request.user == following:
            raise serializers.ValidationError({'following': 'You cannot follow yourself.'})
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def validate_text(self, v):
        if not v or not v.strip():
            raise serializers.ValidationError('Comment text required')
        return v
