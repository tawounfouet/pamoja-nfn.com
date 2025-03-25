from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from model_utils import FieldTracker
from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from authentication.models import User

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        verbose_name_plural = "3. Langues"
        ordering = ['name']

    def __str__(self):
        return self.name

class ContactInfos(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='contact_details')
    
    # Pays de l'utilisateur
    country = CountryField(
        blank_label='(Sélectionnez votre pays)',
        default='FR',
        verbose_name="Pays"
    )
    
    # Phone numbers avec validation
    mobile_phone = PhoneNumberField(
        blank=True, 
        null=True,
        help_text="Format international requis (ex: +33612345678 pour la France)",
    )
    whatsapp_number = PhoneNumberField(
        blank=True, 
        null=True,
        help_text="Format international requis (ex: +33612345678 pour la France)",
    )
    
    # Emails
    contact_email = models.EmailField(blank=True, null=True)
    
    CONTACT_PREFERENCES = [
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('whatsapp', 'WhatsApp'),
    ]
    preferred_contact = models.CharField(
        max_length=10,
        choices=CONTACT_PREFERENCES,
        default='whatsapp'
    )

    def save(self, *args, **kwargs):
        """Surcharge de save pour appeler clean() avant la sauvegarde"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Contacts de {self.profile.user.username}"

    class Meta:
        verbose_name = "2. Informations de contact"
        verbose_name_plural = "2. Informations de contact"

class Socialinks(models.Model):

    class Meta:
        #verbose_name = "3. Liens sociaux"
        verbose_name_plural = "3. Liens sociaux"

    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='social_links')
    facebook = models.URLField(blank=True, null=True, default=None)
    instagram = models.URLField(blank=True, null=True, default=None)
    twitter = models.URLField(blank=True, null=True, default=None)
    linkedin = models.URLField(blank=True, null=True, default=None)

class Profile(models.Model):

    class Meta:
        verbose_name_plural = "1. Profiles utilisateurs"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_profiles'
    )
    languages = models.ManyToManyField(Language)
    #location = models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True)
    last_active = models.DateTimeField(auto_now=True)
    reputation_score = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    tracker = FieldTracker(fields=['verified'])

    @property
    def contact_infos(self):
        """
        Retourne les informations de contact ou None si elles n'existent pas
        """
        try:
            return self.contact_details
        except ContactInfos.DoesNotExist:
            return None

    @property
    def social_links(self):
        """
        Retourne les liens sociaux ou None s'ils n'existent pas
        """
        try:
            return self.social_links
        except Socialinks.DoesNotExist:
            return None

    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    @property
    def is_complete(self):
        """
        Vérifie si le profil est complet selon certains critères
        """
        required_fields = [
            self.bio,
            self.profile_image,
            self.contact_infos,
            self.languages.exists(),
            self.location
        ]
        return all(required_fields)

    @property
    def completion_percentage(self):
        """
        Calcule le pourcentage de complétion du profil
        """
        fields = [
            bool(self.bio),
            bool(self.profile_image),
            bool(self.contact_infos),
            self.languages.exists(),
            bool(self.location),
            bool(self.social_links)
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)

    @property
    def is_recently_active(self):
        """
        Vérifie si l'utilisateur était actif dans les dernières 24h
        """
        return self.last_active >= timezone.now() - timedelta(hours=24)

    @property
    def verification_status(self):
        """
        Retourne le statut de vérification détaillé
        """
        if self.verified:
            return {
                'status': 'verified',
                'date': self.verification_date,
                'verified_by': self.verified_by.get_full_name() if self.verified_by else None
            }
        return {'status': 'unverified'}

    @property
    def reputation_level(self):
        """
        Retourne le niveau de réputation basé sur le score
        """
        if self.reputation_score >= 1000:
            return 'expert'
        elif self.reputation_score >= 500:
            return 'advanced'
        elif self.reputation_score >= 100:
            return 'intermediate'
        return 'beginner'

    @property
    def profile_age(self):
        """
        Retourne l'âge du profil en jours
        """
        return (timezone.now() - self.date_registered).days

    @property
    def has_complete_contact_info(self):
        """
        Vérifie si les informations de contact sont complètes
        """
        if not self.contact_infos:
            return False
        return bool(
            self.contact_infos.mobile_phone or 
            self.contact_infos.whatsapp_number or 
            self.contact_infos.contact_email
        )

    @property
    def primary_language(self):
        """
        Retourne la première langue de l'utilisateur
        """
        return self.languages.first()

    def get_social_presence(self):
        """
        Retourne un dictionnaire des réseaux sociaux actifs
        """
        if not self.social_links:
            return {}
        
        return {
            platform: getattr(self.social_links, platform)
            for platform in ['facebook', 'instagram', 'twitter', 'linkedin']
            if getattr(self.social_links, platform)
        }

    def verify(self, verified_by_user):
        self.verified = True
        self.verification_date = timezone.now()
        self.verified_by = verified_by_user
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
