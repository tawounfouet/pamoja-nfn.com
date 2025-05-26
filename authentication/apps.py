from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
    verbose_name = "1. Gestion des utilisateurs"

    def ready(self):
        import authentication.signals  # Importe les signaux
