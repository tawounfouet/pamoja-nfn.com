#!/usr/bin/env python
"""
Script d'initialisation pour le système d'authentification.
Ce script configure tous les éléments nécessaires pour que l'authentification fonctionne:
- Configure le site par défaut
- Crée les applications sociales (Google, GitHub)
- Vérifie les paramètres

Utilisation:
  python setup_auth_system.py
"""

import os
import sys
import subprocess
import django

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import après la configuration de Django
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


def check_settings():
    """Vérifie que tous les paramètres nécessaires sont configurés"""
    print("\n=== Vérification des paramètres ===")

    # Vérifications JWT
    has_jwt_settings = hasattr(settings, "SIMPLE_JWT")
    print(f"✓ Paramètres JWT configurés: {has_jwt_settings}")

    # Vérifications REST_AUTH
    has_rest_auth = hasattr(settings, "REST_AUTH")
    print(f"✓ Paramètres REST_AUTH configurés: {has_rest_auth}")

    # Vérifications adaptateurs
    has_account_adapter = (
        hasattr(settings, "ACCOUNT_ADAPTER")
        and settings.ACCOUNT_ADAPTER == "authentication.adapters.CustomAccountAdapter"
    )
    has_socialaccount_adapter = (
        hasattr(settings, "SOCIALACCOUNT_ADAPTER")
        and settings.SOCIALACCOUNT_ADAPTER
        == "authentication.adapters.CustomSocialAccountAdapter"
    )
    print(
        f"✓ Adaptateurs personnalisés configurés: {has_account_adapter and has_socialaccount_adapter}"
    )

    # Vérifications clés API
    has_google_keys = bool(
        getattr(settings, "GOOGLE_CLIENT_ID", None)
        and getattr(settings, "GOOGLE_SECRET", None)
    )
    has_github_keys = bool(
        getattr(settings, "GITHUB_CLIENT_ID", None)
        and getattr(settings, "GITHUB_SECRET", None)
    )
    print(f"✓ Clés Google configurées: {has_google_keys}")
    print(f"✓ Clés GitHub configurées: {has_github_keys}")

    return all(
        [
            has_jwt_settings,
            has_rest_auth,
            has_account_adapter,
            has_socialaccount_adapter,
        ]
    )


def configure_site():
    """Configure le site par défaut"""
    print("\n=== Configuration du site ===")

    try:
        # Exécuter le script de configuration du site
        subprocess.run(["python", "authentication/configure_site.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la configuration du site: {e}")
        return False

    return True


def create_social_apps():
    """Crée les applications sociales"""
    print("\n=== Configuration des applications sociales ===")

    try:
        # Exécuter le script de reset des applications sociales
        subprocess.run(["python", "authentication/reset_social_apps.py"], check=True)
        print("✓ Applications sociales configurées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la configuration des applications sociales: {e}")
        return False


def run_migrations():
    """Exécute les migrations nécessaires"""
    print("\n=== Exécution des migrations ===")

    try:
        subprocess.run(["python", "manage.py", "migrate"], check=True)
        print("✓ Migrations exécutées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution des migrations: {e}")
        return False


def test_api():
    """Exécute le script de test de l'API"""
    print("\n=== Test de l'API d'authentification ===")
    print("Voulez-vous exécuter les tests d'API ? (o/n)")
    choice = input().strip().lower()

    if choice == "o" or choice == "oui":
        try:
            subprocess.run(["python", "authentication/test_auth_api.py"], check=False)
            print("✓ Tests exécutés")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution des tests: {e}")
    else:
        print("Tests ignorés")


def cleanup_social_apps():
    """Nettoie les applications sociales dupliquées"""
    print("\n=== Nettoyage des applications sociales ===")
    try:
        subprocess.run(["python", "authentication/cleanup_social_apps.py"], check=True)
        print("✓ Applications sociales nettoyées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du nettoyage des applications sociales: {e}")
        return False


if __name__ == "__main__":
    print("=== Initialisation du système d'authentification ===")

    # Vérification des paramètres
    if not check_settings():
        print("⚠️ Certains paramètres sont manquants. Vérifiez votre configuration.")

    # Configuration du site
    configure_site()

    # Exécution des migrations
    run_migrations()

    # Nettoyage des applications sociales (pour éviter les doublons)
    cleanup_social_apps()

    # Création/mise à jour des applications sociales
    create_social_apps()

    # Test de l'API
    test_api()

    print("\n=== Initialisation terminée ===")
    print(
        "Le système d'authentification est maintenant configuré et prêt à être utilisé."
    )
    print("Pour utiliser l'API, voir la documentation dans README.md")
