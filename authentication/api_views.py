from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount
from .serializers import UserWithSocialAccountsSerializer, SocialAccountSerializer

User = get_user_model()


class UserInfoView(APIView):
    """
    Vue pour obtenir les détails de l'utilisateur actuel avec les comptes sociaux associés
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Récupère les détails de l'utilisateur connecté
        """
        serializer = UserWithSocialAccountsSerializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data)


class SocialAccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les comptes sociaux de l'utilisateur
    """

    serializer_class = SocialAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)
