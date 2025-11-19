from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Engagement, Like, Comment, Follow


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('id', 'follower', 'created_at')


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
