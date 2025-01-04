from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

from authentication.models import User
from .models import Profile, Notification

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée un profil automatiquement pour chaque nouvel utilisateur"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def handle_profile_update(sender, instance, created, **kwargs):
    """Gère les mises à jour de profil"""
    if not created:
        # Invalider le cache
        cache_keys = [
            f'profile_{instance.id}',
            f'profile_search_{instance.user.email}',
        ]
        cache.delete_many(cache_keys)

        # Vérifier les changements importants
        if instance.tracker.has_changed('verified'):
            if instance.verified:
                Notification.create_notification(
                    user=instance.user,
                    notification_type='PROFILE_VERIFIED',
                    title="Profil vérifié",
                    message="Votre profil a été vérifié avec succès !",
                    priority=2
                )

@receiver(post_save, sender=Notification)
def handle_notification_creation(sender, instance, created, **kwargs):
    """Gère la création de notifications"""
    if created:
        # Mettre à jour le compteur de notifications non lues
        cache_key = f'unread_notifications_{instance.user.id}'
        cache.delete(cache_key)

        # Envoyer un email si nécessaire
        if instance.priority >= 2 and not instance.is_email_sent:
            try:
                # Logique d'envoi d'email ici
                instance.is_email_sent = True
                instance.save(update_fields=['is_email_sent'])
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email: {e}")

@receiver(post_delete, sender=Profile)
def handle_profile_deletion(sender, instance, **kwargs):
    """Nettoie les ressources associées lors de la suppression d'un profil"""
    # Supprimer l'image de profil si elle existe
    if instance.profile_image:
        instance.profile_image.delete(save=False)

    # Nettoyer le cache
    cache_keys = [
        f'profile_{instance.id}',
        f'profile_search_{instance.user.email}',
    ]
    cache.delete_many(cache_keys) 