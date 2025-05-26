#!/usr/bin/env python
"""
Script simple pour corriger définitivement le problème des SocialApps en
supprimant toutes les applications existantes et en créant une seule pour chaque provider.

Utilisation:
  python fix_social_apps.py
"""

import os
import sys
import django

# Ajouter le chemin du projet pour pouvoir importer les settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.db import transaction


def fix_social_apps():
    """Correction définitive des SocialApps"""

    print("\n=== Correction des applications sociales ===")

    try:
        # Récupérer le site par défaut
        try:
            site = Site.objects.get(id=1)
            print(f"Site trouvé: {site.name} ({site.domain})")
        except Site.DoesNotExist:
            site = Site.objects.create(
                domain="localhost:8000", name="Pamoja NFN Platform"
            )
            print(f"Site créé: {site.name} ({site.domain})")

        # Définir les providers et les données par défaut
        providers_data = {
            "google": {
                "name": "Google",
                "client_id": "google-client-id-placeholder",
                "secret": "google-secret-placeholder",
            },
            "github": {
                "name": "GitHub",
                "client_id": "github-client-id-placeholder",
                "secret": "github-secret-placeholder",
            },
            "facebook": {
                "name": "Facebook",
                "client_id": "facebook-client-id-placeholder",
                "secret": "facebook-secret-placeholder",
            },
            "linkedin_oauth2": {
                "name": "LinkedIn",
                "client_id": "linkedin-client-id-placeholder",
                "secret": "linkedin-secret-placeholder",
            },
        }

        with transaction.atomic():
            # Supprimer toutes les applications sociales
            print("Suppression de toutes les applications sociales...")
            SocialApp.objects.all().delete()

            # Créer une nouvelle application pour chaque provider
            for provider, data in providers_data.items():
                app = SocialApp.objects.create(
                    provider=provider,
                    name=data["name"],
                    client_id=data["client_id"],
                    secret=data["secret"],
                )
                app.sites.add(site)
                print(f"Application {data['name']} créée (ID: {app.id})")

        print("\n=== Vérification des applications ===")
        for app in SocialApp.objects.all().order_by("provider"):
            sites_str = ", ".join([f"{s.id}:{s.domain}" for s in app.sites.all()])
            print(
                f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: [{sites_str}]"
            )

        print("\n=== Applications sociales corrigées avec succès ===")
        return True

    except Exception as e:
        print(f"Erreur lors de la correction des applications sociales: {e}")
        return False


if __name__ == "__main__":
    fix_social_apps()
