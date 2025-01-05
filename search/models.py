from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class SearchDocument(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)
    
    # Métadonnées pour améliorer la recherche
    tags = models.JSONField(default=list)
    location = models.JSONField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='search_history'
    )
    query = models.CharField(max_length=255)
    filters = models.JSONField(default=dict)
    results_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "search histories"
