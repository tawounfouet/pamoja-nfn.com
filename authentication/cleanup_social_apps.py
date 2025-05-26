#!/usr/bin/env python
"""
Script pour nettoyer les entrées dupliquées des applications sociales dans la base de données.

Utilisation:
  python cleanup_social_apps.py
"""

import os
import sys
import subprocess
import django

# Ajouter le chemin du projet pour pouvoir importer les settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def cleanup_social_apps():
    """Nettoie les entrées dupliquées des SocialApp"""

    print("\n=== Nettoyage des applications sociales ===")

    try:
        # Exécuter le script de reset des applications sociales
        # Ce script supprime toutes les applications existantes et en crée de nouvelles
        subprocess.run(["python", "authentication/reset_social_apps.py"], check=True)
        print("✓ Applications sociales nettoyées avec succès")
        return True
    except Exception as e:
        print(f"Erreur lors du nettoyage des applications sociales: {e}")
        return False


if __name__ == "__main__":
    cleanup_social_apps()
