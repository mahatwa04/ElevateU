from django.apps import AppConfig


class EngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engagement'
    verbose_name = 'Engagement'

    def ready(self):
        # import signals to wire up post_save/post_delete handlers
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
