from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import F
from users.models import Notification, NotificationType
from .models import Message, Conversation

@receiver(post_save, sender=Message)
def notify_new_message(sender, instance, created, **kwargs):
    """
    Envoie une notification au destinataire lors de la création d'un nouveau message
    Met à jour la date de dernière modification de la conversation
    """
    if created:
        # Récupère le destinataire (l'autre participant de la conversation)
        recipient = instance.conversation.get_other_participant(instance.sender)
        
        # Crée une notification pour le destinataire
        Notification.create_notification(
            user=recipient,
            notification_type=NotificationType.NEW_MESSAGE,
            title="Nouveau message",
            message=f"Nouveau message de {instance.sender.username}",
            related_object=instance
        )

        # Met à jour la date de la conversation
        instance.conversation.updated_at = timezone.now()
        instance.conversation.save()

@receiver(pre_save, sender=Message)
def handle_message_status_change(sender, instance, **kwargs):
    """
    Gère les changements de statut des messages
    """
    if not instance.pk:  # Nouveau message
        return

    old_instance = Message.objects.get(pk=instance.pk)
    
    # Si le message vient d'être lu
    if instance.status == Message.Status.READ and old_instance.status != Message.Status.READ:
        instance.read_at = timezone.now()
    
    # Si le message passe à délivré
    elif instance.status == Message.Status.DELIVERED and old_instance.status == Message.Status.SENT:
        # Logique additionnelle si nécessaire pour la livraison
        pass

@receiver(post_save, sender=Conversation)
def create_system_message(sender, instance, created, **kwargs):
    """
    Crée un message système lors de la création d'une nouvelle conversation
    """
    if created:
        participants = instance.participants.all()
        if len(participants) == 2:  # Vérifie qu'il y a bien 2 participants
            Message.objects.create(
                conversation=instance,
                sender=participants[0],  # Utilise le premier participant comme émetteur
                content=f"Début de la conversation entre {participants[0].username} et {participants[1].username}",
                status=Message.Status.READ
            )

@receiver(post_save, sender=Message)
def update_conversation_timestamp(sender, instance, created, **kwargs):
    """
    Met à jour le timestamp de la conversation à chaque nouveau message
    """
    if created:
        instance.conversation.save()  # Cela déclenchera auto_now sur updated_at 