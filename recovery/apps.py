from django.apps import AppConfig


class RecoveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recovery'

    def ready(self):
        import recovery.signals  