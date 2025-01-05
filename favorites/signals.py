from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Favorite
from users.models import Notification, NotificationType

@receiver(post_save, sender=Favorite)
def notify_favorite_created(sender, instance, created, **kwargs):
    if created:
        # Si l'objet favori est un profil ou un listing, notifier son propriétaire
        if hasattr(instance.content_object, 'user'):
            Notification.create_notification(
                user=instance.content_object.user,
                notification_type=NotificationType.NEW_FAVORITE,
                title="Nouveau favori !",
                message=f"{instance.user.username} a ajouté votre contenu à ses favoris",
                related_object=instance.content_object
            ) 