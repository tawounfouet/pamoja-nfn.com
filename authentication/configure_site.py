#!/usr/bin/env python
"""
Ce script configure le site par défaut pour Django Allauth, nécessaire pour
que l'authentification sociale fonctionne correctement.

Utilisation:
  python configure_site.py
"""

import os
import sys
import django

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import après la configuration de Django
from django.contrib.sites.models import Site


def configure_default_site():
    """Configure le site par défaut avec un nom et domaine appropriés"""
    try:
        # Récupère le site par défaut (ID = 1)
        site = Site.objects.get(id=1)

        # Met à jour avec les informations du site actuel
        site.name = "Pamoja NFN Platform"
        site.domain = "localhost:8000"  # En développement

        # En production, changer pour le vrai domaine
        # site.domain = 'pamoja-nfn.com'

        site.save()

        print(f"Site par défaut configuré avec succès: {site.name} ({site.domain})")

    except Site.DoesNotExist:
        # Crée un nouveau site si aucun n'existe avec ID=1
        site = Site.objects.create(
            id=1, name="Pamoja NFN Platform", domain="localhost:8000"
        )
        print(f"Site par défaut créé avec succès: {site.name} ({site.domain})")


if __name__ == "__main__":
    configure_default_site()
