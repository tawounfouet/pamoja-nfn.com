from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from ..models import Profile, Language, SocialMediaPlatform
from ..serializers import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    SocialLinkUpdateSerializer
)

User = get_user_model()

class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.profile = self.user.profile
        self.language = Language.objects.create(name='Français', code='fr')
        self.platform = SocialMediaPlatform.objects.create(
            name='Twitter',
            base_url='https://twitter.com'
        )
        self.profile.languages.add(self.language)
        self.profile.social_media_platforms.add(self.platform)

    def test_profile_serialization(self):
        """Test la sérialisation d'un profil"""
        serializer = ProfileSerializer(self.profile)
        data = serializer.data

        self.assertEqual(data['user_email'], self.user.email)
        self.assertEqual(data['full_name'], 'John Doe')
        self.assertEqual(len(data['languages']), 1)
        self.assertEqual(data['languages'][0]['code'], 'fr')

    def test_profile_update_serialization(self):
        """Test la mise à jour d'un profil via le sérialiseur"""
        data = {
            'bio': 'Nouvelle bio',
            'contact_info': {
                'email': 'contact@test.com',
                'phone': '+33612345678'
            },
            'is_public': True
        }
        serializer = ProfileUpdateSerializer(
            self.profile,
            data=data,
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_profile = serializer.save()

        self.assertEqual(updated_profile.bio, data['bio'])
        self.assertEqual(
            updated_profile.contact_info['email'],
            data['contact_info']['email']
        )

    def test_invalid_contact_info(self):
        """Test la validation des informations de contact invalides"""
        data = {
            'contact_info': {
                'invalid_key': 'value'
            }
        }
        serializer = ProfileUpdateSerializer(
            self.profile,
            data=data,
            partial=True
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('contact_info', serializer.errors)

class SocialLinkUpdateSerializerTests(TestCase):
    def setUp(self):
        self.platform = SocialMediaPlatform.objects.create(
            name='Twitter',
            base_url='https://twitter.com'
        )

    def test_valid_social_link(self):
        """Test la validation d'un lien social valide"""
        data = {
            'platform': 'Twitter',
            'username': 'testuser'
        }
        serializer = SocialLinkUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_platform(self):
        """Test la validation d'une plateforme invalide"""
        data = {
            'platform': 'InvalidPlatform',
            'username': 'testuser'
        }
        serializer = SocialLinkUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('platform', serializer.errors) 