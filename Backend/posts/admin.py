from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'like_count', 'comment_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')