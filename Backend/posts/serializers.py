from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'description', 'category', 'image', 'created_at', 'updated_at', 'like_count', 'comment_count')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'like_count', 'comment_count')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
