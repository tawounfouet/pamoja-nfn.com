#!/usr/bin/env python
"""
Script de correction direct pour les applications sociales - Version simplifiée
"""

import os
import sys
import django

# Configuration de l'environnement Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import après la configuration de Django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


def fix_social_apps_simple():
    """Solution directe pour le problème des applications sociales"""

    try:
        # 1. Afficher l'état initial
        print("\n=== État initial ===")
        print("Sites:")
        for site in Site.objects.all():
            print(f"  ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

        print("\nApplications sociales:")
        for app in SocialApp.objects.all():
            sites = ", ".join([f"{s.id}" for s in app.sites.all()])
            print(
                f"  ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: [{sites}]"
            )

        # 2. Supprimer toutes les applications sociales
        print("\n=== Suppression des applications sociales ===")
        SocialApp.objects.all().delete()
        print("Toutes les applications sociales ont été supprimées.")

        # 3. Vérifier et configurer le site par défaut
        print("\n=== Configuration du site par défaut ===")
        site, created = Site.objects.get_or_create(
            id=1, defaults={"domain": "localhost:8000", "name": "Pamoja NFN Platform"}
        )

        if created:
            print(f"Nouveau site créé: {site.name} ({site.domain})")
        else:
            print(f"Site existant utilisé: {site.name} ({site.domain})")

        # 4. Créer des nouvelles applications sociales
        print("\n=== Création des nouvelles applications sociales ===")
        providers = [
            ("google", "Google", "google-id-placeholder", "google-secret-placeholder"),
            ("github", "GitHub", "github-id-placeholder", "github-secret-placeholder"),
            (
                "facebook",
                "Facebook",
                "facebook-id-placeholder",
                "facebook-secret-placeholder",
            ),
            (
                "linkedin_oauth2",
                "LinkedIn",
                "linkedin-id-placeholder",
                "linkedin-secret-placeholder",
            ),
        ]

        for provider_id, name, client_id, secret in providers:
            app = SocialApp.objects.create(
                provider=provider_id, name=name, client_id=client_id, secret=secret
            )
            app.sites.add(site)
            print(f"Application '{name}' créée avec ID={app.id}")

        # 5. Afficher l'état final
        print("\n=== État final ===")
        print("Applications sociales:")
        for app in SocialApp.objects.all():
            sites = ", ".join([f"{s.id}" for s in app.sites.all()])
            print(
                f"  ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: [{sites}]"
            )

        print("\n=== Correction terminée avec succès ===")

    except Exception as e:
        print(f"Erreur: {e}")


if __name__ == "__main__":
    print("Démarrage de la correction des applications sociales...")
    fix_social_apps_simple()
    print("Script terminé.")
