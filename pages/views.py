from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Profile
from listing.models import Listing
from django.db.models import Count
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer le terme de recherche
        search_query = self.request.GET.get('q', '')
        
        if search_query:
            # Recherche dans les profils
            profiles = Profile.objects.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(bio__icontains=search_query)
            ).distinct()

            # Recherche dans les annonces
            listings = Listing.objects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()

            context['search_results'] = {
                'profiles': profiles[:5],  # Limiter à 5 résultats
                'listings': listings[:5],  # Limiter à 5 résultats
                'total_profiles': profiles.count(),
                'total_listings': listings.count(),
                'query': search_query
            }
        
        # Statistiques
        context['total_users'] = Profile.objects.count()
        context['total_listings'] = Listing.objects.count()
        context['total_countries'] = Profile.objects.exclude(
            contact_details__country=None
        ).values('contact_details__country').distinct().count()
        context['verified_users'] = Profile.objects.filter(verified=True).count()
        
        # Dernières annonces
        context['latest_listings'] = Listing.objects.filter(
            status='active'
        ).order_by('-created_at')[:3]
        
        # Profils mis en avant
        context['featured_profiles'] = Profile.objects.filter(
            verified=True,
            is_public=True
        ).order_by('-reputation_score')[:4]
        
        return context