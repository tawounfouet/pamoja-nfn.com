from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    """
    Signal déclenché lorsqu'un utilisateur s'inscrit
    """
    user = kwargs.get("user")
    if user:
        # Actions à effectuer lors de l'inscription
        pass


@receiver(social_account_added)
def handle_social_account_added(sender, **kwargs):
    """
    Signal déclenché lorsqu'un compte social est ajouté à un utilisateur
    """
    account = kwargs.get("sociallogin")
    if account:
        user = account.user
        provider = account.account.provider
        # Actions à effectuer lors de l'ajout d'un compte social
        print(f"Compte {provider} ajouté pour {user.email}")


@receiver(social_account_updated)
def handle_social_account_updated(sender, **kwargs):
    """
    Signal déclenché lorsqu'un compte social est mis à jour
    """
    account = kwargs.get("sociallogin")
    if account:
        user = account.user
        provider = account.account.provider
        # Actions à effectuer lors de la mise à jour d'un compte social
        print(f"Compte {provider} mis à jour pour {user.email}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal pour créer un profil utilisateur après la création d'un compte
    """
    if created:
        # Si le signal est relié à un modèle Profile, vous pourriez créer un profil ici
        pass
