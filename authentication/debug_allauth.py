#!/usr/bin/env python
"""
Script de débogage pour vérifier les providers allauth
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

# Import après la configuration de Django
from allauth.socialaccount.providers import registry

print("=== Providers disponibles ===")
for provider in registry.get_list():
    print(f"- {provider.id} ({provider.name})")

print("\n=== Analyse du registry ===")
print(f"Registry length: {len(registry.get_list())}")
print(f"Registry unique IDs: {len(set([p.id for p in registry.get_list()]))}")

# Vérifier les doublons
provider_count = {}
for provider in registry.get_list():
    provider_count[provider.id] = provider_count.get(provider.id, 0) + 1

print("\n=== Doublons détectés ===")
for provider_id, count in provider_count.items():
    if count > 1:
        print(f"Provider {provider_id} apparaît {count} fois")

print("\n=== Fin du débogage ===")
