from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache

from .models import Profile, Notification, NotificationType
from authentication.models import User

class ProfileService:
    @staticmethod
    def search_profiles(query, filters=None, user=None):
        """
        Recherche des profils avec des filtres optionnels
        """
        profiles = Profile.objects.filter(is_public=True)

        if query:
            profiles = profiles.filter(
                Q(user__email__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(bio__icontains=query)
            )

        if filters:
            if 'languages' in filters:
                profiles = profiles.filter(languages__code__in=filters['languages'])
            if 'location' in filters:
                profiles = profiles.filter(location=filters['location'])
            if 'verified' in filters:
                profiles = profiles.filter(verified=filters['verified'])

        # Exclure le profil de l'utilisateur courant si spécifié
        if user:
            profiles = profiles.exclude(user=user)

        return profiles.distinct()

    @staticmethod
    def update_profile_reputation(profile, points, reason=None):
        """
        Met à jour le score de réputation d'un profil
        """
        old_score = profile.reputation_score
        profile.update_reputation(points)

        # Créer une notification
        Notification.create_notification(
            user=profile.user,
            notification_type=NotificationType.REPUTATION_CHANGE,
            title="Changement de réputation",
            message=f"Votre réputation a {'augmenté' if points > 0 else 'diminué'} de {abs(points)} points. {reason if reason else ''}",
            priority=1 if abs(points) >= 10 else 0
        )

        return profile.reputation_score - old_score

    @staticmethod
    def record_profile_view(profile, viewer=None):
        """
        Enregistre une vue de profil et gère les notifications
        """
        cache_key = f"profile_view_{profile.id}_{viewer.id if viewer else 'anonymous'}"
        
        # Vérifier si le profil a déjà été vu récemment
        if not cache.get(cache_key):
            # Créer une notification si le viewer est authentifié
            if viewer and viewer != profile.user:
                Notification.create_notification(
                    user=profile.user,
                    notification_type=NotificationType.PROFILE_VIEWED,
                    title="Votre profil a été consulté",
                    message=f"{viewer.get_full_name()} a consulté votre profil",
                    priority=0
                )

            # Mettre en cache pour éviter les notifications multiples
            cache.set(cache_key, True, timeout=3600)  # 1 heure

class NotificationService:
    @staticmethod
    def get_user_notifications(user, unread_only=False, limit=None):
        """
        Récupère les notifications d'un utilisateur
        """
        notifications = Notification.objects.filter(user=user)
        
        if unread_only:
            notifications = notifications.filter(read=False)
            
        if limit:
            notifications = notifications[:limit]
            
        return notifications

    @staticmethod
    def mark_notifications_as_read(user, notification_ids=None):
        """
        Marque les notifications comme lues
        """
        notifications = Notification.objects.filter(user=user, read=False)
        
        if notification_ids:
            notifications = notifications.filter(id__in=notification_ids)
            
        notifications.update(read=True)
        
        return notifications.count() 