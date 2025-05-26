#!/usr/bin/env python
"""
Script pour nettoyer et recréer les applications sociales dans la base de données.
Ce script supprime toutes les applications sociales existantes et en crée de nouvelles.

Utilisation:
  python reset_social_apps.py
"""

import os
import sys
import django

# Ajouter le chemin du projet pour pouvoir importer les settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Importer les modèles après avoir configuré Django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


def reset_social_apps():
    """Supprime toutes les applications sociales et en crée de nouvelles"""

    print("\n=== Suppression et recréation des applications sociales ===")

    # Récupérer le site par défaut
    try:
        site = Site.objects.get(id=1)
        print(f"Site trouvé: {site.name} ({site.domain})")
    except Site.DoesNotExist:
        print("Erreur: Pas de site avec ID 1. Créez d'abord un site.")
        return False

    # Supprimer toutes les applications sociales existantes
    print("Suppression de toutes les applications sociales existantes...")
    SocialApp.objects.all().delete()
    print("Applications sociales supprimées.")

    # Créer l'application Google
    google_app = SocialApp.objects.create(
        provider="google",
        name="Google",
        client_id=getattr(settings, "GOOGLE_CLIENT_ID", ""),
        secret=getattr(settings, "GOOGLE_SECRET", ""),
    )
    google_app.sites.add(site)
    print(f"Application Google créée (ID: {google_app.id})")

    # Créer l'application GitHub
    github_app = SocialApp.objects.create(
        provider="github",
        name="GitHub",
        client_id=getattr(settings, "GITHUB_CLIENT_ID", ""),
        secret=getattr(settings, "GITHUB_SECRET", ""),
    )
    github_app.sites.add(site)
    print(f"Application GitHub créée (ID: {github_app.id})")

    # Créer l'application Facebook
    facebook_app = SocialApp.objects.create(
        provider="facebook",
        name="Facebook",
        client_id=getattr(settings, "FACEBOOK_CLIENT_ID", ""),
        secret=getattr(settings, "FACEBOOK_SECRET", ""),
    )
    facebook_app.sites.add(site)
    print(f"Application Facebook créée (ID: {facebook_app.id})")

    # Créer l'application LinkedIn
    linkedin_app = SocialApp.objects.create(
        provider="linkedin_oauth2",
        name="LinkedIn",
        client_id=getattr(settings, "LINKEDIN_CLIENT_ID", ""),
        secret=getattr(settings, "LINKEDIN_SECRET", ""),
    )
    linkedin_app.sites.add(site)
    print(f"Application LinkedIn créée (ID: {linkedin_app.id})")

    # Vérification finale
    print("\nVérification des applications sociales:")
    for app in SocialApp.objects.all().order_by('id'):
        site_ids = [str(site.id) for site in app.sites.all()]
        print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: {', '.join(site_ids)}")

    return True


if __name__ == "__main__":
    reset_social_apps()
    print("\n=== Terminé ===")
