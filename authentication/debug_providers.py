#!/usr/bin/env python

"""
Script simple pour vérifier les providers dans la base de données
"""

import os
import sys
import django

# Configuration
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

# Ne pas oublier d'initialiser Django
django.setup()

# Imports
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from allauth.socialaccount.providers import registry

# Afficher les fournisseurs enregistrés
print("=== FOURNISSEURS ENREGISTRÉS ===")
providers = registry.get_list()
for provider in providers:
    print(f"- {provider.id}: {provider.name}")

print("\n=== APPLICATIONS SOCIALES EN BASE DE DONNÉES ===")
apps = SocialApp.objects.all().order_by("provider")
print(f"Nombre total: {apps.count()}")

for app in apps:
    sites = ", ".join([f"{s.domain}" for s in app.sites.all()])
    print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: [{sites}]")

# C'est probablement ici que vient le bug - regardons ce que retourne get_list
print("\n=== TEST TAG get_providers ===")
from allauth.socialaccount.templatetags.socialaccount import get_providers

providers = get_providers()
print(f"Nombre de providers retournés: {len(providers)}")
for provider in providers:
    print(f"- {provider.id}: {provider.name}")

# Vérifier s'il y a des doublons dans les ID de provider
print("\n=== VÉRIFICATION DOUBLONS ===")
provider_ids = [p.id for p in providers]
unique_ids = set(provider_ids)
print(f"IDs uniques: {len(unique_ids)}, Total: {len(provider_ids)}")
if len(unique_ids) != len(provider_ids):
    print("ATTENTION: Des doublons ont été trouvés!")
    from collections import Counter

    duplicates = [item for item, count in Counter(provider_ids).items() if count > 1]
    print(f"IDs dupliqués: {duplicates}")

print("\n=== FIN ===")
