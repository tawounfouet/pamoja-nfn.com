from rest_framework import permissions


class IsAuthenticatedForWriteOrReadOnly(permissions.BasePermission):
    """
    Permet l'accès en lecture à tous les utilisateurs (connectés ou non),
    mais exige l'authentification pour toute action d'écriture.
    """

    def has_permission(self, request, view):
        # Autoriser toutes les requêtes en lecture
        if request.method in permissions.SAFE_METHODS:
            return True

        # Exiger l'authentification pour les requêtes d'écriture
        return request.user and request.user.is_authenticated
