#!/usr/bin/env python
"""
Script pour nettoyer et reconfigurer les applications sociales dans la base de données
en utilisant directement des requêtes SQL pour plus de fiabilité.

Utilisation:
  python fix_social_apps_sql.py
"""

import os
import sys
import sqlite3
import django

# Ajouter le chemin du projet pour pouvoir importer les settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings


def get_database_path():
    """Obtient le chemin de la base de données SQLite"""
    databases = getattr(settings, "DATABASES", {})
    default_db = databases.get("default", {})
    engine = default_db.get("ENGINE", "")

    if "sqlite3" in engine:
        return default_db.get("NAME")

    return None


def fix_social_apps():
    """Correction des applications sociales par SQL direct"""

    db_path = get_database_path()
    if not db_path:
        print("Base de données SQLite non trouvée dans les paramètres")
        return False

    print(f"Base de données trouvée: {db_path}")

    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Supprimer toutes les relations SocialApp-Site
        print("1. Suppression des relations SocialApp-Site...")
        cursor.execute("DELETE FROM socialaccount_socialapp_sites")

        # 2. Supprimer toutes les applications sociales
        print("2. Suppression des applications sociales...")
        cursor.execute("DELETE FROM socialaccount_socialapp")

        # 3. Vérifier l'existence du site par défaut
        print("3. Vérification du site par défaut...")
        cursor.execute("SELECT id, domain, name FROM django_site WHERE id=1")
        site = cursor.fetchone()

        if not site:
            print("Création du site par défaut...")
            cursor.execute(
                """
                INSERT INTO django_site (id, domain, name) 
                VALUES (1, 'localhost:8000', 'Pamoja NFN Platform')
            """
            )
            site_id = 1
        else:
            site_id = site[0]
            print(f"Site trouvé: ID={site_id}, Domain={site[1]}, Name={site[2]}")

        # 4. Créer les applications sociales
        print("4. Création des nouvelles applications sociales...")
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
            # Insérer l'application
            cursor.execute(
                """
                INSERT INTO socialaccount_socialapp (provider, name, client_id, secret, key)
                VALUES (?, ?, ?, ?, ?)
            """,
                (provider_id, name, client_id, secret, ""),
            )

            # Récupérer l'ID généré
            cursor.execute("SELECT last_insert_rowid()")
            app_id = cursor.fetchone()[0]

            # Associer l'application au site
            cursor.execute(
                """
                INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id)
                VALUES (?, ?)
            """,
                (app_id, site_id),
            )

            print(
                f"Application '{name}' créée avec ID={app_id} et associée au site ID={site_id}"
            )

        # Valider les changements
        conn.commit()

        # Vérifier l'état final
        print("\n5. Vérification finale de l'état:")

        cursor.execute(
            """
            SELECT sa.id, sa.provider, sa.name, sa.client_id, s.id, s.domain
            FROM socialaccount_socialapp sa
            JOIN socialaccount_socialapp_sites sas ON sa.id = sas.socialapp_id
            JOIN django_site s ON sas.site_id = s.id
            ORDER BY sa.provider
        """
        )

        apps = cursor.fetchall()
        for app in apps:
            print(
                f"ID: {app[0]}, Provider: {app[1]}, Name: {app[2]}, Client ID: {app[3]}, Site: {app[4]}:{app[5]}"
            )

        conn.close()
        print("\n=== Applications sociales corrigées avec succès ===")
        return True

    except Exception as e:
        print(f"Erreur lors de la correction des applications sociales: {e}")
        if "conn" in locals():
            conn.rollback()
            conn.close()
        return False


if __name__ == "__main__":
    fix_social_apps()
