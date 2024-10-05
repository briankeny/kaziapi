from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
   
   # Import the signals module
   
    def ready(self):
        import authentication.signals  