from rest_framework import permissions

class IsProfileOwner(permissions.BasePermission):
    """
    Permission permettant uniquement au propriétaire du profil de le modifier
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsProfilePublic(permissions.BasePermission):
    """
    Permission permettant l'accès aux profils publics ou au propriétaire
    """
    def has_object_permission(self, request, view, obj):
        return obj.is_public or obj.user == request.user 