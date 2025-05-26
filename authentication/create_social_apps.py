#!/usr/bin/env python
"""
Script pour générer des fixtures pour les SocialApp Django Allauth.
Cela permet de configurer facilement les fournisseurs OAuth comme Google et GitHub.

Utilisation:
  python create_social_apps.py
"""

import os
import json
import sys
import django

# Ajouter le chemin du projet pour pouvoir importer les settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Importer les modèles après avoir configuré Django
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


def create_social_app_fixture():
    """Crée un fichier de fixture pour les SocialApp"""

    # Récupérer le site par défaut
    try:
        site = Site.objects.get(id=1)
    except Site.DoesNotExist:
        print("Erreur: Pas de site avec ID 1. Créez d'abord un site.")
        return

    # Configuration des applications sociales
    social_apps = [
        {
            "model": "socialaccount.socialapp",
            "pk": 1,
            "fields": {
                "provider": "google",
                "name": "Google",
                "client_id": "{{GOOGLE_CLIENT_ID}}",
                "secret": "{{GOOGLE_SECRET}}",
                "key": "",
                "sites": [site.id],
            },
        },
        {
            "model": "socialaccount.socialapp",
            "pk": 2,
            "fields": {
                "provider": "github",
                "name": "GitHub",
                "client_id": "{{GITHUB_CLIENT_ID}}",
                "secret": "{{GITHUB_SECRET}}",
                "key": "",
                "sites": [site.id],
            },
        },
        # Ajoutez d'autres fournisseurs au besoin
    ]

    # Écrire le fichier de fixture
    with open("authentication/fixtures/socialapps.json", "w") as f:
        json.dump(social_apps, f, indent=2)

    print("Fixture créé avec succès: authentication/fixtures/socialapps.json")
    print(
        "Remplacez les placeholders {{GOOGLE_CLIENT_ID}}, etc. par vos vraies informations d'API"
    )
    print(
        "Ensuite, chargez les fixtures avec: python manage.py loaddata authentication/fixtures/socialapps.json"
    )


def create_real_social_apps():
    """Crée directement les applications sociales dans la base de données"""
    # Récupérer le site par défaut
    try:
        site = Site.objects.get(id=1)
    except Site.DoesNotExist:
        print("Erreur: Pas de site avec ID 1. Créez d'abord un site.")
        return

    from django.conf import settings

    # Google - vérifier s'il existe déjà une application Google
    try:
        google_apps = SocialApp.objects.filter(provider="google")
        if google_apps.exists():
            # Utiliser la première application Google existante
            google_app = google_apps.first()
            google_app.name = "Google"
            google_app.client_id = getattr(settings, "GOOGLE_CLIENT_ID", "")
            google_app.secret = getattr(settings, "GOOGLE_SECRET", "")
            google_app.save()

            # S'assurer que le site est associé
            if site not in google_app.sites.all():
                google_app.sites.add(site)
            print(f"Application Google mise à jour (ID: {google_app.id})")
        else:
            # Créer une nouvelle application
            google_app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id=getattr(settings, "GOOGLE_CLIENT_ID", ""),
                secret=getattr(settings, "GOOGLE_SECRET", ""),
            )
            google_app.sites.add(site)
            print(f"Application Google créée (ID: {google_app.id})")
    except Exception as e:
        print(f"Erreur lors de la création/mise à jour de l'application Google: {e}")

    # GitHub - vérifier s'il existe déjà une application GitHub
    try:
        github_apps = SocialApp.objects.filter(provider="github")
        if github_apps.exists():
            # Utiliser la première application GitHub existante
            github_app = github_apps.first()
            github_app.name = "GitHub"
            github_app.client_id = getattr(settings, "GITHUB_CLIENT_ID", "")
            github_app.secret = getattr(settings, "GITHUB_SECRET", "")
            github_app.save()

            # S'assurer que le site est associé
            if site not in github_app.sites.all():
                github_app.sites.add(site)
            print(f"Application GitHub mise à jour (ID: {github_app.id})")
        else:
            # Créer une nouvelle application
            github_app = SocialApp.objects.create(
                provider="github",
                name="GitHub",
                client_id=getattr(settings, "GITHUB_CLIENT_ID", ""),
                secret=getattr(settings, "GITHUB_SECRET", ""),
            )
            github_app.sites.add(site)
            print(f"Application GitHub créée (ID: {github_app.id})")
    except Exception as e:
        print(f"Erreur lors de la création/mise à jour de l'application GitHub: {e}")


if __name__ == "__main__":
    # Créer le répertoire des fixtures s'il n'existe pas
    os.makedirs("authentication/fixtures", exist_ok=True)

    # Option 1: Créer un fichier de fixture
    create_social_app_fixture()

    # Option 2: Créer directement les applications dans la base de données
    # create_real_social_apps()
