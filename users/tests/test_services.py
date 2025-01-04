from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from ..models import Profile, Language, Notification
from ..services import ProfileService, NotificationService

User = get_user_model()

class ProfileServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile
        self.language = Language.objects.create(name='Français', code='fr')
        self.profile.languages.add(self.language)

    def tearDown(self):
        cache.clear()

    def test_search_profiles(self):
        """Test la recherche de profils"""
        # Créer quelques profils pour le test
        user2 = User.objects.create_user(
            email='test2@example.com',
            password='testpass123',
            first_name='Jean',
            last_name='Dupont'
        )
        profile2 = user2.profile
        profile2.bio = "Développeur Python"
        profile2.save()

        # Test recherche par nom
        results = ProfileService.search_profiles('Jean')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), profile2)

        # Test recherche par compétence
        results = ProfileService.search_profiles('Python')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), profile2)

        # Test filtrage par langue
        filters = {'languages': ['fr']}
        results = ProfileService.search_profiles('', filters=filters)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.profile)

    def test_update_profile_reputation(self):
        """Test la mise à jour de la réputation"""
        initial_score = self.profile.reputation_score
        points = 10
        reason = "Contribution exceptionnelle"

        change = ProfileService.update_profile_reputation(
            self.profile,
            points,
            reason
        )

        self.assertEqual(change, points)
        self.profile.refresh_from_db()
        self.assertEqual(
            self.profile.reputation_score,
            initial_score + points
        )

        # Vérifier la création de la notification
        notification = Notification.objects.filter(
            user=self.user,
            notification_type='REPUTATION_CHANGE'
        ).first()
        self.assertIsNotNone(notification)
        self.assertIn(str(points), notification.message)
        self.assertIn(reason, notification.message)

    def test_record_profile_view(self):
        """Test l'enregistrement des vues de profil"""
        viewer = User.objects.create_user(
            email='viewer@example.com',
            password='testpass123'
        )

        # Premier vue
        ProfileService.record_profile_view(self.profile, viewer)
        notification = Notification.objects.filter(
            user=self.user,
            notification_type='PROFILE_VIEWED'
        ).first()
        self.assertIsNotNone(notification)

        # Deuxième vue dans l'heure - ne devrait pas créer de nouvelle notification
        ProfileService.record_profile_view(self.profile, viewer)
        notification_count = Notification.objects.filter(
            user=self.user,
            notification_type='PROFILE_VIEWED'
        ).count()
        self.assertEqual(notification_count, 1)

class NotificationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        # Créer quelques notifications
        for i in range(5):
            Notification.create_notification(
                user=self.user,
                notification_type='TEST',
                title=f'Test {i}',
                message=f'Message {i}'
            )

    def test_get_user_notifications(self):
        """Test la récupération des notifications"""
        # Test sans filtre
        notifications = NotificationService.get_user_notifications(self.user)
        self.assertEqual(notifications.count(), 5)

        # Test avec limite
        notifications = NotificationService.get_user_notifications(
            self.user,
            limit=3
        )
        self.assertEqual(len(notifications), 3)

        # Test notifications non lues uniquement
        notifications = NotificationService.get_user_notifications(
            self.user,
            unread_only=True
        )
        self.assertEqual(notifications.count(), 5)

    def test_mark_notifications_as_read(self):
        """Test le marquage des notifications comme lues"""
        # Marquer toutes les notifications comme lues
        count = NotificationService.mark_notifications_as_read(self.user)
        self.assertEqual(count, 5)

        # Vérifier qu'il n'y a plus de notifications non lues
        unread = Notification.objects.filter(
            user=self.user,
            read=False
        ).count()
        self.assertEqual(unread, 0)

        # Test avec des IDs spécifiques
        new_notif = Notification.create_notification(
            user=self.user,
            notification_type='TEST',
            title='New Test',
            message='New Message'
        )
        count = NotificationService.mark_notifications_as_read(
            self.user,
            notification_ids=[new_notif.id]
        )
        self.assertEqual(count, 1) 