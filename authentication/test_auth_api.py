#!/usr/bin/env python
"""
Script de test pour les endpoints d'authentification.
Ce script effectue une série de requêtes pour tester l'API d'authentification.

Utilisation:
  python test_auth_api.py
"""

import os
import sys
import requests
import json

# URL de base pour les tests
BASE_URL = "http://localhost:8000/api/auth/"

# Informations pour l'inscription d'un utilisateur de test
TEST_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "first_name": "Test",
    "last_name": "User",
}


def print_response(response, title):
    """Affiche proprement une réponse HTTP"""
    print(f"\n--- {title} ---")
    print(f"Status Code: {response.status_code}")

    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except ValueError:
        print(response.text)

    print("-" * 60)


def test_registration():
    """Teste l'endpoint d'inscription"""
    url = f"{BASE_URL}auth/registration/"
    response = requests.post(url, json=TEST_USER)
    print_response(response, "Test d'inscription")
    return response


def test_login():
    """Teste l'endpoint de connexion"""
    url = f"{BASE_URL}auth/login/"
    data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
    response = requests.post(url, json=data)
    print_response(response, "Test de connexion")

    # Extraire le token pour les tests suivants
    token = None
    try:
        token = response.json().get("access_token")
    except:
        pass

    return token


def test_user_details(token):
    """Teste l'endpoint de détails utilisateur"""
    url = f"{BASE_URL}me/"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(url, headers=headers)
    print_response(response, "Détails de l'utilisateur")


def test_jwt():
    """Teste les endpoints JWT"""
    # Obtenir un token JWT
    url = f"{BASE_URL}jwt/create/"
    data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
    response = requests.post(url, json=data)
    print_response(response, "Obtention de token JWT")

    # Extraire les tokens
    try:
        data = response.json()
        access_token = data.get("access")
        refresh_token = data.get("refresh")

        if access_token:
            # Vérifier le token
            verify_url = f"{BASE_URL}jwt/verify/"
            verify_response = requests.post(verify_url, json={"token": access_token})
            print_response(verify_response, "Vérification du token JWT")

            # Rafraîchir le token
            refresh_url = f"{BASE_URL}jwt/refresh/"
            refresh_response = requests.post(
                refresh_url, json={"refresh": refresh_token}
            )
            print_response(refresh_response, "Rafraîchissement du token JWT")
    except:
        print("Erreur pendant les tests JWT")


if __name__ == "__main__":
    print("Démarrage des tests de l'API d'authentification...")

    # Tester l'inscription (commentez cette ligne si l'utilisateur existe déjà)
    # Vous pourriez recevoir une erreur 400 si l'utilisateur existe déjà
    test_registration()

    # Tester la connexion
    token = test_login()

    if token:
        # Tester les détails de l'utilisateur avec le token
        test_user_details(token)
    else:
        print("Impossible d'obtenir un token, test des détails de l'utilisateur ignoré")

    # Tester les endpoints JWT
    test_jwt()

    print("\nTests terminés.")
