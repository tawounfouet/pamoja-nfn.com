from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Profile, Language, SocialMediaPlatform, Notification

User = get_user_model()

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.language = Language.objects.create(name='Français', code='fr')
        self.platform = SocialMediaPlatform.objects.create(
            name='Twitter',
            base_url='https://twitter.com'
        )

    def test_profile_creation(self):
        """Test la création automatique du profil"""
        self.assertIsInstance(self.user.profile, Profile)

    def test_social_link_management(self):
        """Test l'ajout et la récupération des liens sociaux"""
        username = 'testuser'
        self.profile.add_social_link('Twitter', username)
        social_links = self.profile.get_social_links()
        
        self.assertIn('Twitter', social_links)
        self.assertEqual(
            social_links['Twitter'],
            f'https://twitter.com/{username}'
        )

    def test_contact_info_validation(self):
        """Test la validation des informations de contact"""
        valid_info = {
            'email': 'contact@test.com',
            'phone': '+33612345678'
        }
        self.profile.update_contact_info(**valid_info)
        self.assertEqual(self.profile.contact_info['email'], valid_info['email'])

    def test_reputation_update(self):
        """Test la mise à jour du score de réputation"""
        initial_score = self.profile.reputation_score
        points = 10
        self.profile.update_reputation(points)
        self.assertEqual(
            self.profile.reputation_score,
            initial_score + points
        )

class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_notification_creation(self):
        """Test la création de notification"""
        notification = Notification.create_notification(
            user=self.user,
            notification_type='PROFILE_VERIFIED',
            title="Test Notification",
            message="Test message",
            priority=1
        )
        
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.title, "Test Notification")
        self.assertFalse(notification.read)

    def test_mark_as_read(self):
        """Test le marquage d'une notification comme lue"""
        notification = Notification.create_notification(
            user=self.user,
            notification_type='PROFILE_VERIFIED',
            title="Test Notification",
            message="Test message"
        )
        
        notification.mark_as_read()
        self.assertTrue(notification.read) 