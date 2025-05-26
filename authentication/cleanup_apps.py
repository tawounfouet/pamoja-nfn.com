#!/usr/bin/env python
"""
Script super simplifié pour nettoyer les apps sociales
"""
import django
import os
import sys
import traceback

try:
    print("Démarrage du script...")

    # Setup Django
    print("Configuration de Django...")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"
    print("Environ DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))

    django.setup()
    print("Django configuré.")

    # Imports Django
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site

    # Nettoyage
    print("Suppression de toutes les applications sociales...")
    SocialApp.objects.all().delete()
    print("Applications supprimées.")
except Exception as e:
    print("ERREUR:", str(e))
    print("Traceback:")
    traceback.print_exc()

# Récupération du site
site, _ = Site.objects.get_or_create(id=1)
print(f"Site: {site.domain}")

# Création des nouvelles apps
providers = [
    ("google", "Google", "client_id", "secret"),
    ("github", "GitHub", "client_id", "secret"),
    ("facebook", "Facebook", "client_id", "secret"),
    ("linkedin_oauth2", "LinkedIn", "client_id", "secret"),
]

print("Création des nouvelles applications sociales:")
for provider, name, client_id, secret in providers:
    app = SocialApp.objects.create(
        provider=provider, name=name, client_id=client_id, secret=secret
    )
    app.sites.add(site)
    print(f"- {name} (ID: {app.id})")

print("Terminé!")
