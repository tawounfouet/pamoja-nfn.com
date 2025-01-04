from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Profile, Language, Notification

User = get_user_model()

class ProfileViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.profile = self.user.profile
        self.language = Language.objects.create(name='Français', code='fr')

    def test_profile_list(self):
        """Test la liste des profils publics"""
        url = reverse('users:profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_detail(self):
        """Test la récupération d'un profil"""
        url = reverse('users:profile-detail', args=[self.profile.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_email'], self.user.email)

    def test_profile_update(self):
        """Test la mise à jour d'un profil"""
        url = reverse('users:profile-detail', args=[self.profile.id])
        data = {
            'bio': 'Nouvelle bio',
            'is_public': True
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Nouvelle bio')

    def test_profile_search(self):
        """Test la recherche de profils"""
        url = reverse('users:profile-search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class NotificationViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.create_notification(
            user=self.user,
            notification_type='TEST',
            title='Test Notification',
            message='Test message'
        )

    def test_notification_list(self):
        """Test la liste des notifications"""
        url = reverse('users:notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_notification_read(self):
        """Test le marquage d'une notification comme lue"""
        url = reverse('users:notification-mark-read', args=[self.notification.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read) 