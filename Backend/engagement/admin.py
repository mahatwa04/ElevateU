from django.contrib import admin
from .models import Engagement


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'content_type', 'object_id', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__email', 'user__username', 'reaction', 'comment')
