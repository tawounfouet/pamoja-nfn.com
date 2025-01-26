# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import SearchDocument
# from django.contrib.contenttypes.models import ContentType

# @receiver(post_save)
# def update_search_document(sender, instance, **kwargs):
#     if isinstance(instance, SearchDocument):
#         return
        
#     content_type = ContentType.objects.get_for_model(instance)
#     search_doc, created = SearchDocument.objects.get_or_create(
#         content_type=content_type,
#         object_id=instance.pk
#     )
    
#     # Update search fields
#     search_doc.title = str(instance)
#     search_doc.content = str(instance.__dict__)
#     search_doc.search_text = f"{search_doc.title} {search_doc.content}"
#     search_doc.save()