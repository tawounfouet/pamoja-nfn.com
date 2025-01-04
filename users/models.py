from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from authentication.models import User

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    base_url = models.URLField()
    icon = models.CharField(max_length=50)

    def get_full_url(self, username):
        return f"{self.base_url.rstrip('/')}/{username}"

    def __str__(self):
        return self.name

class Profile(models.Model):
    CONTACT_INFO_SCHEMA = {
        'email': str,
        'phone': str,
        'address': str,
        'website': str
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    contact_info = models.JSONField(default=dict)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='verified_profiles'
    )
    social_media_links = models.JSONField(default=dict)
    languages = models.ManyToManyField(Language)
    social_media_platforms = models.ManyToManyField(SocialMediaPlatform)
    location = models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True)
    last_active = models.DateTimeField(auto_now=True)
    reputation_score = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)

    def verify(self, verified_by_user):
        self.verified = True
        self.verification_date = timezone.now()
        self.verified_by = verified_by_user
        self.save()

    def add_social_link(self, platform_name, username):
        try:
            platform = SocialMediaPlatform.objects.get(name=platform_name)
            self.social_media_links[platform_name] = username
            self.save()
            return platform.get_full_url(username)
        except SocialMediaPlatform.DoesNotExist:
            return None

    def get_social_links(self):
        return {
            platform: SocialMediaPlatform.objects.get(name=platform).get_full_url(username)
            for platform, username in self.social_media_links.items()
        }

    def update_contact_info(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.CONTACT_INFO_SCHEMA:
                self.contact_info[key] = value
        self.save()

    def update_reputation(self, points):
        self.reputation_score = max(0, self.reputation_score + points)
        self.save()

    def __str__(self):
        return f"Profile de {self.user.username}"

class NotificationType(models.TextChoices):
    PROFILE_VERIFIED = 'PROFILE_VERIFIED', 'Profile vérifié'
    NEW_MESSAGE = 'NEW_MESSAGE', 'Nouveau message'
    NEW_REVIEW = 'NEW_REVIEW', 'Nouvel avis'
    LISTING_APPROVED = 'LISTING_APPROVED', 'Annonce approuvée'
    PROFILE_VIEWED = 'PROFILE_VIEWED', 'Profil consulté'
    REPUTATION_CHANGE = 'REPUTATION_CHANGE', 'Changement de réputation'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )
    related_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    related_object_id = models.PositiveIntegerField(null=True)
    related_object = GenericForeignKey('related_object_type', 'related_object_id')
    is_email_sent = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['read', 'created_at']),
        ]

    def mark_as_read(self):
        self.read = True
        self.save()

    @classmethod
    def create_notification(cls, user, notification_type, title, message, related_object=None, priority=0):
        notification = cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority
        )
        if related_object:
            notification.related_object = related_object
            notification.save()
        return notification

    def __str__(self):
        return f"Notification pour {self.user.username}: {self.title}"



# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

 
# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User) 