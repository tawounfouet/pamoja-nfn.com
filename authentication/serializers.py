from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    Serializer pour le modèle User avec des détails supplémentaires
    """

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("is_staff", "date_joined")
        read_only_fields = ("email", "username", "is_staff", "date_joined")


class SocialAccountSerializer(serializers.ModelSerializer):
    """
    Serializer pour les informations du compte social
    """

    provider_name = serializers.SerializerMethodField()

    class Meta:
        model = SocialAccount
        fields = ("id", "provider", "provider_name", "uid", "last_login", "date_joined")
        read_only_fields = ("id", "provider", "uid", "last_login", "date_joined")

    def get_provider_name(self, obj):
        return obj.get_provider().name


class UserWithSocialAccountsSerializer(CustomUserDetailsSerializer):
    """
    Serializer qui inclut les comptes sociaux liés à l'utilisateur
    """

    social_accounts = serializers.SerializerMethodField()

    class Meta(CustomUserDetailsSerializer.Meta):
        fields = CustomUserDetailsSerializer.Meta.fields + ("social_accounts",)

    def get_social_accounts(self, obj):
        accounts = SocialAccount.objects.filter(user=obj)
        return SocialAccountSerializer(accounts, many=True).data
