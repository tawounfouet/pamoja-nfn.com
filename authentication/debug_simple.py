#!/usr/bin/env python

"""
Script simple avec gestion d'erreur explcite pour déboguer
"""

import os
import sys
import traceback

try:
    print("Démarrage...")

    # Configurer l'environnement
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

    print("Configuration de l'environnement Django...")
    import django

    django.setup()
    print("Django configuré avec succès.")

    # Importer les modèles
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site

    # Compter les applications
    apps_count = SocialApp.objects.count()
    print(f"Nombre total de SocialApp: {apps_count}")

    # Lister les applications par provider
    for provider in SocialApp.objects.values_list("provider", flat=True).distinct():
        count = SocialApp.objects.filter(provider=provider).count()
        print(f"Provider '{provider}': {count} application(s)")

    # Lister toutes les applications
    print("\nListe des applications:")
    for app in SocialApp.objects.all():
        sites = ", ".join([s.domain for s in app.sites.all()])
        print(f"ID {app.id}: {app.provider} ({app.name}) - Sites: {sites}")

    # Tester le tag template
    print("\nTest du tag get_providers:")
    from allauth.socialaccount.templatetags.socialaccount import get_providers

    providers = get_providers()
    print(f"Nombre de providers retournés: {len(providers)}")
    provider_ids = [p.id for p in providers]

    # Vérifier les doublons
    from collections import Counter

    counts = Counter(provider_ids)
    duplicates = [item for item, count in counts.items() if count > 1]
    print(f"Providers uniques: {len(set(provider_ids))}")
    print(f"Total providers: {len(provider_ids)}")

    if duplicates:
        print("DOUBLONS DÉTECTÉS:")
        for dup in duplicates:
            print(f"- {dup} apparaît {counts[dup]} fois")
            # Les objets avec le même ID
            for i, p in enumerate([p for p in providers if p.id == dup]):
                print(f"  Instance {i+1}: {p} (ID: {id(p)})")

except Exception as e:
    print(f"ERREUR: {str(e)}")
    traceback.print_exc()
    print("\nStacktrace complet:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
