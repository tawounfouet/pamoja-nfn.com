import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Avg

# import SearchVectorField
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

from django.utils.text import slugify

# pip install django-taggit
from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager



from authentication.models import User
from users.models import Profile
from location.models import Location






class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True , null=True)


    description = models.TextField(default="", blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "1. Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_active_listings_count(self):
        return self.listing_set.filter(status=Listing.Status.ACTIVE).count()

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)

    class Meta:
        verbose_name_plural = "2. Sous-categories"
        unique_together = ['category', 'name']
        ordering = ['category', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(unique=True)
#     category = models.ForeignKey(
#         Category, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True,
#         related_name='tags'
#     )

#     class Meta:
#         ordering = ['name']

#     def __str__(self):
#         return self.name



class CustomTag(TagBase):
    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

# This intermediate model is needed for custom tags
class TaggedListing(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="tagged_listings"
    )


class ContactInformation(models.Model):

    class Meta:
        verbose_name_plural = "6. Informations de contact"

    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, related_name='contact_details')
    
    # Phone numbers
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    
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
        default='email'
    )

class SocialMediaLinks(models.Model):

    class Meta:
        verbose_name_plural = "7. Réseaux sociaux"

    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, related_name='social_media')
    facebook = models.URLField(blank=True, null=True, default=None)
    instagram = models.URLField(blank=True, null=True, default=None)
    twitter = models.URLField(blank=True, null=True, default=None)
    linkedin = models.URLField(blank=True, null=True, default=None)


class BusinessHours(models.Model):

    class Meta:
        verbose_name_plural = "8. Horaires d'ouverture"

    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, related_name='operating_hours')
    
    # Monday
    monday_open = models.TimeField(null=True, blank=True)
    monday_close = models.TimeField(null=True, blank=True)
    monday_closed = models.BooleanField(default=False)
    
    # Tuesday
    tuesday_open = models.TimeField(null=True, blank=True)
    tuesday_close = models.TimeField(null=True, blank=True)
    tuesday_closed = models.BooleanField(default=False)
    
    # Wednesday
    wednesday_open = models.TimeField(null=True, blank=True)
    wednesday_close = models.TimeField(null=True, blank=True)
    wednesday_closed = models.BooleanField(default=False)
    
    # Thursday
    thursday_open = models.TimeField(null=True, blank=True)
    thursday_close = models.TimeField(null=True, blank=True)
    thursday_closed = models.BooleanField(default=False)
    
    # Friday
    friday_open = models.TimeField(null=True, blank=True)
    friday_close = models.TimeField(null=True, blank=True)
    friday_closed = models.BooleanField(default=False)
    
    # Saturday
    saturday_open = models.TimeField(null=True, blank=True)
    saturday_close = models.TimeField(null=True, blank=True)
    saturday_closed = models.BooleanField(default=False)
    
    # Sunday
    sunday_open = models.TimeField(null=True, blank=True)
    sunday_close = models.TimeField(null=True, blank=True)
    sunday_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Business Hours for {self.listing}"



class Listing(models.Model):
    class Types(models.TextChoices):
        INDIVIDUAL = 'IND', 'Individuel'
        COMPANY = 'COM', 'Entreprise'

    class Status(models.TextChoices):
        ACTIVE = 'ACT', 'Actif'
        INACTIVE = 'INA', 'Inactif'
        PENDING = 'PEN', 'En attente de validation'

    def get_default_contact_info():
        return {
            "phone": {
                "primary": None,
                "mobile": None,
                "whatsapp": None
            },
            "email": {
                "primary": None,
                "support": None
            },
            "social_media": {
                "facebook": None,
                "instagram": None,
                "twitter": None,
                "linkedin": None
            },
            "messaging": {
                "telegram": None,
                "whatsapp": None,
                "messenger": None
            },
            "preferred_contact": "email"
        }

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='listings')
    owner = models.CharField(max_length=200, default="Pamoja", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=3, choices=Types.choices)
    title = models.CharField(max_length=200, default="")
    company_name = models.CharField(max_length=200, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='listings', null=True)
    description = models.TextField(blank=True, null=True, default="")
    #contact_info = models.JSONField()
    # contact_info = models.JSONField(
    #     default=get_default_contact_info,
    #     null=True,
    #     blank=True,
    #     help_text="Contact information including phone, email, and social media links"
    # )
    logo = models.ImageField(upload_to='listing_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website_url = models.URLField(blank=True, null=True, default="")
    #business_hours = models.JSONField(default=None, blank=True, null=True)
    status = models.CharField(
        max_length=3, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    #tags = models.ManyToManyField(Tag, related_name='listings')
    #tags = models.ManyToManyField(CustomTag, related_name='listings')

    tags = TaggableManager(
        through=TaggedListing,
        blank=True,
        help_text="List of tags for this listing",
        to=CustomTag  # Explicitly use CustomTag model
    )


    #search_vector = SearchVectorField(null=True, blank=True)  # For PostgreSQL full-text search
    search_vector = SearchVectorField(
        null=True, 
        blank=True,
        help_text="PostgreSQL full-text search vector"
    )
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['search_vector']),
    #     ]

    

    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True, 
        null=True, 
        default=None,
        help_text="Unique URL identifier"
    )
    def generate_slug(self):
        if not self.slug:
            uuid_str = str(uuid.uuid4())[:5]
            self.slug = slugify(self.title) + '-' + uuid_str

    def save(self, *args, **kwargs):
        self.generate_slug()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "3. Annonces"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['status']),
            models.Index(fields=['type']),
            #GinIndex(fields=['search_vector']),
            models.Index(fields=['search_vector']),
            models.Index(fields=['slug']),
        ]
        ordering = ['-created_at']

    def get_cache_key(self):
        return f"listing_{self.id}_data"
    
    
    def get_contact_info(self):
        return self.contact_details

    def update_average_rating(self):
        """Met à jour la note moyenne du listing"""
        avg_rating = self.reviews.filter(
            is_visible=True
        ).aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg_rating or 0.0
        self.save(update_fields=['average_rating'])

    def get_business_hours_display(self):
        """Retourne les horaires d'ouverture formatés"""
        # Logique de formatage des horaires
        return self.business_hours

    def is_open_now(self):
        """Vérifie si l'établissement est ouvert actuellement"""
        # Logique de vérification des horaires
        pass

    @property
    def contact_infos(self):
        """Returns a dictionary of all contact information for the listing"""
        contact_info = {}
        
        if hasattr(self, 'contact_details'):
            contact = self.contact_details
            contact_info.update({
                'mobile_phone': contact.mobile_phone,
                'whatsapp_number': contact.whatsapp_number,
                'contact_email': contact.contact_email,
                'preferred_contact': contact.preferred_contact
            })
        
        if hasattr(self, 'social_media'):
            social = self.social_media
            contact_info.update({
                'facebook': social.facebook,
                'instagram': social.instagram,
                'twitter': social.twitter,
                'linkedin': social.linkedin
            })
        
        return contact_info

    def __str__(self):
        return f"{self.company_name or self.profile.user.username} - {self.category.name}"

class Review(models.Model):

    # class Meta:
    #     verbose_name_plural = "4. Avis"
    class ModerationStatus(models.TextChoices):
        PENDING = 'PEN', 'En attente'
        APPROVED = 'APP', 'Approuvé'
        REJECTED = 'REJ', 'Rejeté'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    moderation_status = models.CharField(
        max_length=3,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PENDING
    )
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "4. Avis"
        unique_together = ['user', 'listing']
        indexes = [
            models.Index(fields=['moderation_status']),
            models.Index(fields=['is_visible']),
        ]

    def approve(self):
        """Approuve l'avis et met à jour la note moyenne"""
        self.moderation_status = self.ModerationStatus.APPROVED
        self.is_visible = True
        self.save()
        self.listing.update_average_rating()

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.listing}"

class Media(models.Model):

    # class Meta:
    #     verbose_name_plural = "9. Médias"

    class Types(models.TextChoices):
        IMAGE = 'IMG', 'Image'
        DOCUMENT = 'DOC', 'Document'
        VIDEO = 'VID', 'Vidéo'

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='listing_media/')
    type = models.CharField(max_length=3, choices=Types.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "9. Medias"
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f"{self.get_type_display()} pour {self.listing}"

class Analytics(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    engagement_metrics = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)

    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views += 1
        self.save(update_fields=['views', 'last_updated'])

    def update_engagement(self, metric_type, value=1):
        """Met à jour les métriques d'engagement"""
        if metric_type not in self.engagement_metrics:
            self.engagement_metrics[metric_type] = 0
        self.engagement_metrics[metric_type] += value
        self.save(update_fields=['engagement_metrics', 'last_updated'])

    class Meta:
        verbose_name_plural = "5. Statistiques"

    def __str__(self):
        return f"Analytics pour {self.listing}"
