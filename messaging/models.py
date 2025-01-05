from django.db import models
from django.conf import settings
from django.utils import timezone



class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def get_other_participant(self, user):
        """Retourne l'autre participant de la conversation"""
        return self.participants.exclude(id=user.id).first()

    def __str__(self):
        participants = self.participants.all()
        return f"Conversation entre {participants[0]} et {participants[1]}"

class Message(models.Model):
    class Status(models.TextChoices):
        SENT = 'SENT', 'Envoyé'
        DELIVERED = 'DELV', 'Délivré'
        READ = 'READ', 'Lu'

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.SENT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'status']),
        ]

    def mark_as_read(self):
        """Marque le message comme lu"""
        if self.status != self.Status.READ:
            self.status = self.Status.READ
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])

    def mark_as_delivered(self):
        """Marque le message comme délivré"""
        if self.status == self.Status.SENT:
            self.status = self.Status.DELIVERED
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Message de {self.sender} dans {self.conversation}"

class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='message_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pièce jointe: {self.file_name}"
