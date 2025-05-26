from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Adaptateur personnalisé pour les comptes allauth
    """

    def is_open_for_signup(self, request: HttpRequest):
        """
        Vérifie si l'inscription est ouverte
        """
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_email_confirmation_redirect_url(self, request):
        """
        URL de redirection après confirmation d'email
        """
        if request.user.is_authenticated:
            return settings.LOGIN_REDIRECT_URL
        return settings.LOGIN_URL


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptateur personnalisé pour les comptes sociaux
    """

    def is_open_for_signup(self, request: HttpRequest, sociallogin):
        """
        Vérifie si l'inscription via réseaux sociaux est ouverte
        """
        return getattr(settings, "SOCIALACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(self, request, sociallogin, data):
        """
        Remplit les informations de l'utilisateur à partir des données sociales
        """
        user = super().populate_user(request, sociallogin, data)

        # Si l'avatar est disponible, l'ajouter à l'utilisateur
        social_account = sociallogin.account
        if social_account.provider == "google":
            picture_url = social_account.extra_data.get("picture")
            if picture_url:
                # Vous pourriez enregistrer cette URL ou télécharger l'image
                # Nécessite une modification du modèle User pour stocker l'avatar
                pass

        return user

    def get_app(self, request, provider, client_id=None):
        """
        Surcharge de la méthode get_app pour éviter l'erreur MultipleObjectsReturned
        Cette méthode retourne l'application sociale pour un provider donné.
        """
        from allauth.socialaccount.models import SocialApp

        try:
            # Essayer de récupérer toutes les applications pour ce provider
            apps = self.list_apps(request, provider=provider, client_id=client_id)

            if len(apps) > 1:
                # En cas de multiple applications pour le même provider,
                # retourner la première sans lever d'exception
                app_to_keep = apps[0]
                print(
                    f"Found multiple apps for provider {provider}, using app ID: {app_to_keep.id}"
                )
                return app_to_keep

            # Si une seule app, la retourner
            elif len(apps) == 1:
                return apps[0]

            # Si aucune app, lever l'exception standard
            else:
                raise SocialApp.DoesNotExist(
                    f"No SocialApp found for provider {provider}"
                )

        except Exception as e:
            # Capturer et tracer toutes les exceptions qui pourraient se produire
            print(f"Error in get_app for provider {provider}: {str(e)}")
            # Réessayer avec la méthode par défaut
            return super().get_app(request, provider, client_id)
