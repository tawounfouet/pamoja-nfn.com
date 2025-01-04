from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db import transaction
from django.core.cache import cache

from utils.ip_utils import IPInfoHandler
from utils.jwt_utils import JWTHandler

from .models import (
    User, 
    UserSession, 
    SecurityEvent, 
    LoginHistory,
    EmailVerification,
    TrustedDevice,
    AuthToken,
    PhoneVerification,
    LoginAttempt,
    SecurityPreference,
    RevokedToken
)

# Initialiser les gestionnaires
ip_handler = IPInfoHandler()
jwt_handler = JWTHandler()

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """Gère les événements post-connexion"""
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Obtenir les détails de localisation
    ip_details = ip_handler.get_ip_details(ip_address)
    location = f"{ip_details.get('city', '')}, {ip_details.get('country', '')}" if ip_details else ''

    with transaction.atomic():
        # Créer une nouvelle session
        session = UserSession.objects.create(
            user=user,
            session_key=request.session.session_key,
            ip_address=ip_address,
            user_agent=user_agent,
            location=location
        )

        # Générer le token JWT
        token = jwt_handler.generate_token_pair(
            user_id=user.id,
            session_id=session.id
        )
        session.token = token['access']
        session.save()

        # Créer l'historique de connexion
        LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=session.device_type,
            location=location
        )

@receiver(user_logged_out)
def on_user_logout(sender, request, user, **kwargs):
    """Gère les événements de déconnexion"""
    if not user:
        return

    session_key = request.session.session_key
    if session_key:
        session = UserSession.objects.filter(
            user=user,
            session_key=session_key,
            is_active=True
        ).first()

        if session:
            # Révoquer le token JWT
            if session.token:
                jwt_handler.revoke_token(session.token, reason="Déconnexion utilisateur")
            
            session.end_session()

@receiver(post_save, sender=User)
def handle_user_update(sender, instance, created, **kwargs):
    """Gère les mises à jour du profil utilisateur"""
    if not created:
        # Vérifier les changements critiques
        critical_changes = []
        
        if instance.tracker.has_changed('email'):
            critical_changes.append('email')
            # Créer une nouvelle vérification d'email
            EmailVerification.objects.create(user=instance)

        if instance.tracker.has_changed('phone_number'):
            critical_changes.append('téléphone')
            # Créer une nouvelle vérification de téléphone
            PhoneVerification.objects.create(user=instance)

        if critical_changes:
            SecurityEvent.log_event(
                user=instance,
                event_type=SecurityEvent.EventType.SECURITY_CHANGE,
                description=f"Modifications critiques: {', '.join(critical_changes)}",
                severity=3
            )

@receiver(post_save, sender=SecurityPreference)
def handle_security_preferences(sender, instance, created, **kwargs):
    """Gère les changements de préférences de sécurité"""
    if not created:
        SecurityEvent.log_event(
            user=instance.user,
            event_type=SecurityEvent.EventType.SECURITY_CHANGE,
            description="Modification des préférences de sécurité",
            severity=1
        )
        
        # Appliquer les nouvelles préférences
        if instance.max_sessions:
            instance.clean_old_sessions()

# Signaux liés aux vérifications
@receiver(post_save, sender=EmailVerification)
def handle_email_verification(sender, instance, created, **kwargs):
    """Gère le processus de vérification d'email"""
    if created:
        # Envoyer l'email de vérification
        context = {
            'user': instance.user,
            'verification': instance,
            'expiration': instance.expires_at
        }
        
        html_message = render_to_string(
            'authentication/emails/verify_email.html',
            context
        )
        
        send_mail(
            subject='Vérifiez votre adresse email',
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email]
        )
    
    elif instance.is_verified and not instance.verified_at:
        # Email vérifié avec succès
        instance.verified_at = timezone.now()
        instance.save(update_fields=['verified_at'])
        
        instance.user.email_verified = True
        instance.user.save(update_fields=['email_verified'])

@receiver(post_save, sender=PhoneVerification)
def handle_phone_verification(sender, instance, created, **kwargs):
    """Gère le processus de vérification du téléphone"""
    if created:
        # Envoyer le SMS de vérification
        # Implémenter l'envoi de SMS ici
        pass
    
    elif instance.is_verified and not instance.verified_at:
        instance.verified_at = timezone.now()
        instance.save(update_fields=['verified_at'])
        
        instance.user.phone_verified = True
        instance.user.save(update_fields=['phone_verified'])

# Signaux de nettoyage
@receiver(pre_delete, sender=User)
def handle_user_deletion(sender, instance, **kwargs):
    """Gère la suppression d'un compte utilisateur"""
    # Créer un événement final
    SecurityEvent.log_event(
        user=instance,
        event_type=SecurityEvent.EventType.SECURITY_CHANGE,
        description="Compte utilisateur supprimé",
        severity=3
    )
    
    # Révoquer tous les tokens
    AuthToken.objects.filter(user=instance).update(is_active=False)
    
    # Terminer toutes les sessions
    UserSession.objects.filter(user=instance).update(
        is_active=False,
        expires_at=timezone.now()
    )

# Signaux de monitoring des sessions
@receiver(post_save, sender=UserSession)
def monitor_concurrent_sessions(sender, instance, created, **kwargs):
    """Surveille et gère les sessions concurrentes"""
    if created:
        user = instance.user
        prefs = user.security_preferences

        # Récupérer toutes les sessions actives
        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True
        ).order_by('-created_at')

        # Vérifier les sessions simultanées depuis différentes localisations
        locations = set()
        suspicious_activity = False

        for session in active_sessions:
            if session.location:
                locations.add(session.location)
                if len(locations) > 2:  # Plus de 2 localisations différentes
                    suspicious_activity = True
                    break

        if suspicious_activity:
            SecurityEvent.log_event(
                user=user,
                event_type=SecurityEvent.EventType.SUSPICIOUS_ACTIVITY,
                description="Sessions simultanées depuis plusieurs localisations",
                severity=2,
                ip_address=instance.ip_address,
                device_info=instance.user_agent
            )

        # Appliquer la limite de sessions
        if prefs.max_sessions and active_sessions.count() > prefs.max_sessions:
            # Garder uniquement les sessions les plus récentes
            for old_session in active_sessions[prefs.max_sessions:]:
                old_session.is_active = False
                old_session.expires_at = timezone.now()
                old_session.save()

# Signaux de gestion des tokens
@receiver([post_save, post_delete], sender=AuthToken)
def audit_token_changes(sender, instance, **kwargs):
    """Audit des modifications de tokens"""
    created = kwargs.get('created', False)
    
    if created:
        action = "créé"
    elif 'post_delete' in kwargs.get('signal', ''):
        action = "supprimé"
    else:
        action = "modifié"

    SecurityEvent.log_event(
        user=instance.user,
        event_type=SecurityEvent.EventType.TOKEN_CREATED if created else SecurityEvent.EventType.TOKEN_REVOKED,
        description=f"Token {instance.name} {action}",
        severity=2 if instance.token_type in ['API', 'OAUTH'] else 1,
        related_token=instance if not kwargs.get('raw', False) else None
    )

# Signaux de protection contre les attaques
@receiver(user_login_failed)
def detect_brute_force(sender, credentials, request, **kwargs):
    """Détection avancée des tentatives de force brute"""
    ip_address = request.META.get('REMOTE_ADDR')
    email = credentials.get('username', '')

    # Vérifier les patterns d'attaque
    recent_attempts = LoginAttempt.objects.filter(
        ip_address=ip_address,
        attempt_time__gte=timezone.now() - timezone.timedelta(minutes=5)
    )

    if recent_attempts.count() >= 10:  # 10 tentatives en 5 minutes
        # Bloquer l'IP temporairement
        cache_key = f'ip_blocked_{ip_address}'
        cache.set(cache_key, True, 1800)  # 30 minutes de blocage

        # Créer un événement de sécurité
        user = User.objects.filter(email=email).first()
        if user:
            SecurityEvent.log_event(
                user=user,
                event_type=SecurityEvent.EventType.SUSPICIOUS_ACTIVITY,
                description=f"Possible attaque par force brute depuis {ip_address}",
                severity=3,
                ip_address=ip_address
            )

# Signaux de monitoring des changements critiques
@receiver(pre_save, sender=User)
def monitor_critical_changes(sender, instance, **kwargs):
    """Surveille les changements critiques sur le compte utilisateur"""
    if instance.pk:  # Si l'utilisateur existe déjà
        old_instance = User.objects.get(pk=instance.pk)
        
        critical_changes = []

        # Vérifier les changements critiques
        if old_instance.email != instance.email:
            critical_changes.append(f"Email modifié: {old_instance.email} → {instance.email}")
        
        if old_instance.phone_number != instance.phone_number:
            critical_changes.append(f"Téléphone modifié: {old_instance.phone_number} → {instance.phone_number}")
        
        if old_instance.role != instance.role:
            critical_changes.append(f"Rôle modifié: {old_instance.role} → {instance.role}")
        
        if old_instance.status != instance.status:
            critical_changes.append(f"Statut modifié: {old_instance.status} → {instance.status}")

        if critical_changes:
            # Envoyer une notification à l'utilisateur
            context = {
                'user': instance,
                'changes': critical_changes,
                'date': timezone.now()
            }
            
            html_message = render_to_string(
                'authentication/emails/critical_changes_alert.html',
                context
            )
            
            send_mail(
                subject='Modifications importantes sur votre compte',
                message='',
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[old_instance.email, instance.email]
            )

            # Créer un événement de sécurité
            SecurityEvent.log_event(
                user=instance,
                event_type=SecurityEvent.EventType.SECURITY_CHANGE,
                description=f"Modifications critiques: {', '.join(critical_changes)}",
                severity=3
            )

# Signaux de nettoyage automatique
@receiver(post_save, sender=SecurityEvent)
def cleanup_old_events(sender, **kwargs):
    """Nettoie les anciens événements de sécurité"""
    if not settings.DEBUG:  # Ne pas exécuter en développement
        # Supprimer les événements de plus de 6 mois
        old_date = timezone.now() - timezone.timedelta(days=180)
        SecurityEvent.objects.filter(
            created_at__lt=old_date,
            severity__lt=2  # Garder les événements critiques
        ).delete()

# Signaux de gestion des sessions expirées
@receiver(post_save, sender=UserSession)
def handle_session_expiration(sender, instance, **kwargs):
    """Gère l'expiration des sessions et la synchronisation entre appareils"""
    
    if instance.is_expired and instance.is_active:
        with transaction.atomic():
            # Marquer la session comme inactive
            instance.is_active = False
            instance.save(update_fields=['is_active'])

            # Notifier les autres sessions du même utilisateur
            active_sessions = UserSession.objects.filter(
                user=instance.user,
                is_active=True
            ).exclude(id=instance.id)

            for session in active_sessions:
                # Ajouter un message dans la file d'attente de notifications
                # pour informer les autres sessions
                notification = {
                    'type': 'session_expired',
                    'session_id': instance.id,
                    'device_name': instance.device_type,
                    'timestamp': timezone.now().isoformat()
                }
                
                cache_key = f'session_notifications_{session.session_key}'
                current_notifications = cache.get(cache_key, [])
                current_notifications.append(notification)
                cache.set(cache_key, current_notifications, timeout=3600)

# Signaux de synchronisation des appareils
@receiver(post_save, sender=TrustedDevice)
def sync_device_changes(sender, instance, **kwargs):
    """Synchronise les changements d'appareils entre les sessions"""
    
    if kwargs.get('created'):
        # Nouveau dispositif ajouté
        event_type = 'device_added'
    elif instance.tracker.has_changed('is_trusted'):
        # Statut de confiance modifié
        event_type = 'trust_changed'
    elif instance.tracker.has_changed('trust_score'):
        # Score de confiance modifié
        event_type = 'score_changed'
    else:
        return

    # Notifier toutes les sessions actives
    active_sessions = UserSession.objects.filter(
        user=instance.user,
        is_active=True
    )

    notification = {
        'type': event_type,
        'device_id': instance.device_id,
        'device_name': instance.device_name,
        'is_trusted': instance.is_trusted,
        'trust_score': instance.trust_score,
        'timestamp': timezone.now().isoformat()
    }

    for session in active_sessions:
        cache_key = f'device_sync_{session.session_key}'
        current_updates = cache.get(cache_key, [])
        current_updates.append(notification)
        cache.set(cache_key, current_updates, timeout=3600)

# Signaux de monitoring de la santé des sessions
@receiver(post_save, sender=UserSession)
def monitor_session_health(sender, instance, **kwargs):
    """Surveille la santé des sessions et détecte les anomalies"""
    if not instance.is_active:
        return

    health_issues = []

    # Vérifier les changements d'IP
    if instance.tracker.has_changed('ip_address'):
        old_ip = instance.tracker.previous('ip_address')
        new_ip = instance.ip_address
        
        # Utiliser IPInfo pour la vérification
        distance = ip_handler.calculate_distance(old_ip, new_ip)
        if distance and distance > 500:  # Plus de 500km
            health_issues.append(f"Changement d'IP suspect (distance: {distance:.1f}km)")

        # Vérifier les détails des IPs
        old_details = ip_handler.get_ip_details(old_ip)
        new_details = ip_handler.get_ip_details(new_ip)

        if old_details and new_details:
            # Vérifier le changement de pays
            if old_details.get('country') != new_details.get('country'):
                health_issues.append(f"Changement de pays détecté: {old_details.get('country')} → {new_details.get('country')}")

            # Vérifier le changement de fuseau horaire
            if old_details.get('timezone') != new_details.get('timezone'):
                health_issues.append("Changement de fuseau horaire détecté")

            # Vérifier l'organisation (ASN)
            if old_details.get('org') != new_details.get('org'):
                health_issues.append("Changement de fournisseur d'accès détecté")

    # Vérifier l'activité suspecte
    recent_activity = SecurityEvent.objects.filter(
        user=instance.user,
        created_at__gte=timezone.now() - timezone.timedelta(hours=1),
        severity__gte=2
    ).exists()

    if recent_activity:
        health_issues.append("Activité suspecte récente détectée")

    # Si des problèmes sont détectés
    if health_issues:
        # Créer un événement de sécurité
        SecurityEvent.log_event(
            user=instance.user,
            event_type=SecurityEvent.EventType.SESSION_HEALTH,
            description=f"Problèmes de santé de session détectés: {', '.join(health_issues)}",
            severity=2,
            ip_address=instance.ip_address,
            device_info=instance.user_agent,
            location=instance.location
        )

        # Mettre à jour le score de confiance de l'appareil
        if instance.device:
            instance.device.decrease_trust_score(
                reason="Problèmes de santé de session",
                amount=len(health_issues) * 5
            )

# N'oubliez pas d'ajouter dans apps.py : 