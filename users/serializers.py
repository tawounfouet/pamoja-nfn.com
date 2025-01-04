from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Language, SocialMediaPlatform, Notification

User = get_user_model()

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']

class SocialMediaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaPlatform
        fields = ['id', 'name', 'base_url', 'icon']

class ProfileSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)
    social_media_platforms = SocialMediaPlatformSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'user_email', 'full_name', 'bio', 'contact_info',
            'profile_image', 'date_registered', 'verified',
            'languages', 'social_media_platforms', 'social_links',
            'location', 'last_active', 'reputation_score', 'is_public'
        ]
        read_only_fields = ['id', 'date_registered', 'verified', 'reputation_score']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

    def get_social_links(self, obj):
        return obj.get_social_links()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'read', 'created_at',
            'notification_type', 'priority', 'is_email_sent'
        ]
        read_only_fields = ['id', 'created_at']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Language.objects.all(),
        required=False
    )
    social_media_platforms = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SocialMediaPlatform.objects.all(),
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 'contact_info', 'profile_image',
            'languages', 'social_media_platforms',
            'location', 'is_public'
        ]

    def validate_contact_info(self, value):
        """Valide que les informations de contact respectent le schéma"""
        for key, val in value.items():
            if key not in Profile.CONTACT_INFO_SCHEMA:
                raise serializers.ValidationError(f"Clé invalide: {key}")
            expected_type = Profile.CONTACT_INFO_SCHEMA[key]
            if not isinstance(val, expected_type):
                raise serializers.ValidationError(
                    f"Type invalide pour {key}. Attendu: {expected_type.__name__}"
                )
        return value

class SocialLinkUpdateSerializer(serializers.Serializer):
    platform = serializers.CharField()
    username = serializers.CharField()

    def validate_platform(self, value):
        if not SocialMediaPlatform.objects.filter(name=value).exists():
            raise serializers.ValidationError("Plateforme sociale invalide")
        return value

class ProfileSearchSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.SerializerMethodField()
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user_email', 'full_name', 'bio',
            'profile_image', 'verified', 'languages',
            'location', 'reputation_score'
        ]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() 