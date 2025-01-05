from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from listing.models import Listing
from users.models import Profile

@receiver(post_save, sender=Listing)
@receiver(post_save, sender=Profile)
def update_search_document(sender, instance, **kwargs):
    """Met à jour ou crée le document de recherche pour les objets indexables"""
    from .models import SearchDocument
    
    content_type = ContentType.objects.get_for_model(instance)
    
    with transaction.atomic():
        search_doc, created = SearchDocument.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id
        )
        
        # Personnaliser selon le type d'objet
        if isinstance(instance, Listing):
            search_doc.title = instance.company_name or str(instance)
            search_doc.content = instance.description
            search_doc.tags = [tag.name for tag in instance.tags.all()]
            search_doc.location = {
                'city': instance.location.city,
                'country': instance.location.country
            }
        elif isinstance(instance, Profile):
            search_doc.title = instance.user.username
            search_doc.content = instance.bio
            
        # Mise à jour du vecteur de recherche
        search_doc.search_vector = SearchVector('title', weight='A') + \
                                 SearchVector('content', weight='B')
        search_doc.save() 