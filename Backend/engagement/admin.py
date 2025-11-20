from django.contrib import admin
from .models import Engagement, Like, Comment, Follow


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'content_type', 'object_id', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__email', 'user__username', 'reaction', 'comment')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'post__title')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'post__title', 'text')
    readonly_fields = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__email', 'following__email')
