from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q
from .models import SearchDocument, SearchHistory

class SearchService:
    @staticmethod
    def search(query, user=None, filters=None):
        """
        Effectue une recherche avec filtres optionnels
        """
        search_query = SearchQuery(query, config='french')
        
        # Construction de la requête de base
        base_query = SearchDocument.objects.filter(
            search_vector=search_query
        ).annotate(
            rank=SearchRank('search_vector', search_query)
        )

        # Application des filtres
        if filters:
            if 'location' in filters:
                base_query = base_query.filter(
                    location__city__icontains=filters['location']
                )
            if 'tags' in filters:
                base_query = base_query.filter(
                    tags__contains=filters['tags']
                )

        # Tri par pertinence
        results = base_query.order_by('-rank')

        # Enregistrement de l'historique de recherche
        if user and not user.is_anonymous:
            SearchHistory.objects.create(
                user=user,
                query=query,
                filters=filters or {},
                results_count=results.count()
            )

        return results 