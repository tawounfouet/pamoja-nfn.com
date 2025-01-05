from django.contrib.contenttypes.models import ContentType
from .models import Favorite

class FavoriteService:
    @staticmethod
    def toggle_favorite(user, obj):
        """
        Ajoute ou supprime un favori
        """
        content_type = ContentType.objects.get_for_model(obj)
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.id,
        )
        
        if not created:
            favorite.delete()
            return False
        return True

    @staticmethod
    def get_user_favorites(user, model=None):
        """
        Récupère les favoris d'un utilisateur, optionnellement filtrés par type
        """
        queryset = Favorite.objects.filter(user=user)
        if model:
            content_type = ContentType.objects.get_for_model(model)
            queryset = queryset.filter(content_type=content_type)
        return queryset 