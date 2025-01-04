from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
import uuid
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        if not username:
            raise ValueError('Le nom d\'utilisateur est obligatoire')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Roles.ADMIN)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'USER', 'Simple utilisateur'
        PROVIDER = 'PROVIDER', 'Prestataire'
        ADMIN = 'ADMIN', 'Administrateur'
        MODERATOR = 'MOD', 'Modérateur'
        STAFF = 'STAFF', 'Staff'

    class AccountStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        ACTIVE = 'ACTIVE', 'Actif'
        SUSPENDED = 'SUSPENDED', 'Suspendu'
        BANNED = 'BANNED', 'Banni'

    # Champs de base
    email = models.EmailField(unique=True, verbose_name='Adresse email')
    username = models.CharField(max_length=100, unique=True, verbose_name='Nom d\'utilisateur')
    role = models.CharField(
        max_length=10, 
        choices=Roles.choices, 
        default=Roles.USER,
        verbose_name='Rôle'
    )
    status = models.CharField(
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING,
        verbose_name='Statut du compte'
    )

    # Informations personnelles
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'"
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True,
        verbose_name='Numéro de téléphone'
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        verbose_name='Photo de profil'
    )

    # Paramètres du compte
    is_verified = models.BooleanField(default=False, verbose_name='Compte vérifié')
    email_verified = models.BooleanField(default=False, verbose_name='Email vérifié')
    phone_verified = models.BooleanField(default=False, verbose_name='Téléphone vérifié')
    two_factor_enabled = models.BooleanField(default=False, verbose_name='2FA activé')
    
    # Timestamps
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.CharField(max_length=255, blank=True)
    email_changed_at = models.DateTimeField(null=True, blank=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.username} - {self.email} - {self.role}"

    def save(self, *args, **kwargs):
        if self.pk:
            original = User.objects.get(pk=self.pk)
            if original.email != self.email:
                self.email_verified = False
                self.email_changed_at = timezone.now()
            if original.password != self.password:
                self.password_changed_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_provider(self):
        return self.role == self.Roles.PROVIDER

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    @property
    def requires_password_change(self):
        if not self.password_changed_at:
            return True
        password_max_age = timedelta(days=90)
        return timezone.now() - self.password_changed_at > password_max_age

class EmailVerification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Utilisateur'
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vérification d\'email'
        verbose_name_plural = 'Vérifications d\'email'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_verified']),
        ]

    def __str__(self):
        return f"Vérification pour {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

class PhoneVerification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Utilisateur'
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Vérification de téléphone'
        verbose_name_plural = 'Vérifications de téléphone'
        indexes = [
            models.Index(fields=['user', 'is_verified']),
        ]

    def __str__(self):
        return f"Vérification pour {self.user.phone_number}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def max_attempts_reached(self):
        return self.attempts >= 3

class UserSession(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)
    token = models.TextField(null=True)

    class Meta:
        db_table = 'user_sessions'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
        ]

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def end_session(self, reason=None):
        self.is_active = False
        self.expires_at = timezone.now()
        self.save()

class LoginAttempt(models.Model):
    """Suivi des tentatives de connexion"""
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Réussie'
        FAILED = 'FAILED', 'Échouée'
        BLOCKED = 'BLOCKED', 'Bloquée'

    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.FAILED
    )
    attempt_time = models.DateTimeField(auto_now_add=True)
    failure_reason = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Tentative de connexion'
        verbose_name_plural = 'Tentatives de connexion'
        indexes = [
            models.Index(fields=['email', 'ip_address', 'status']),
            models.Index(fields=['attempt_time']),
        ]

    def __str__(self):
        return f"Tentative de connexion pour {self.email} - {self.status}"

    @classmethod
    def get_recent_failures(cls, email, ip_address, minutes=30):
        time_threshold = timezone.now() - timedelta(minutes=minutes)
        return cls.objects.filter(
            email=email,
            ip_address=ip_address,
            status=cls.Status.FAILED,
            attempt_time__gte=time_threshold
        ).count()

class LoginHistory(models.Model):
    """Historique détaillé des connexions"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_history',
        verbose_name='Utilisateur'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    device_type = models.CharField(max_length=20)
    location = models.CharField(max_length=100, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    session_duration = models.DurationField(null=True, blank=True)
    is_suspicious = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Historique de connexion'
        verbose_name_plural = 'Historique des connexions'
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['user', 'login_time']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['is_suspicious']),
        ]

    def __str__(self):
        return f"Connexion de {self.user.username} le {self.login_time}"

    def save(self, *args, **kwargs):
        if self.logout_time and self.login_time:
            self.session_duration = self.logout_time - self.login_time
        super().save(*args, **kwargs)

    @property
    def is_active_session(self):
        return self.logout_time is None

    def mark_suspicious(self, reason):
        self.is_suspicious = True
        self.notes = f"{self.notes}\n[{timezone.now()}] {reason}".strip()
        self.save()

class SecurityPreference(models.Model):
    """Préférences de sécurité personnalisées par utilisateur"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='security_preferences',
        verbose_name='Utilisateur'
    )
    max_sessions = models.PositiveSmallIntegerField(
        default=5,
        verbose_name='Nombre maximum de sessions simultanées'
    )
    session_timeout = models.PositiveIntegerField(
        default=30,
        help_text='Durée de session en jours'
    )
    notify_on_new_login = models.BooleanField(
        default=True,
        verbose_name='Notification lors d\'une nouvelle connexion'
    )
    notify_on_password_change = models.BooleanField(
        default=True,
        verbose_name='Notification lors d\'un changement de mot de passe'
    )
    allowed_ip_ranges = models.TextField(
        blank=True,
        help_text='Liste des plages IP autorisées (une par ligne)'
    )
    require_2fa_for_new_devices = models.BooleanField(
        default=False,
        verbose_name='2FA requis pour les nouveaux appareils'
    )

    class Meta:
        verbose_name = 'Préférence de sécurité'
        verbose_name_plural = 'Préférences de sécurité'

    def __str__(self):
        return f"Préférences de sécurité de {self.user.username}"

    def is_ip_allowed(self, ip_address):
        if not self.allowed_ip_ranges:
            return True
        # Logique de vérification des plages IP
        return True  # À implémenter selon les besoins

    def clean_old_sessions(self):
        """Nettoie les anciennes sessions si le maximum est atteint"""
        active_sessions = UserSession.objects.filter(
            user=self.user,
            is_active=True
        ).order_by('-last_activity')
        
        if active_sessions.count() > self.max_sessions:
            sessions_to_close = active_sessions[self.max_sessions:]
            for session in sessions_to_close:
                session.is_active = False
                session.save()

class AuthToken(models.Model):
    """Jetons d'authentification pour les API et les intégrations"""
    class TokenType(models.TextChoices):
        API = 'API', 'Clé API'
        OAUTH = 'OAUTH', 'OAuth Token'
        REFRESH = 'REFRESH', 'Refresh Token'
        RESET = 'RESET', 'Reset Password'
        TEMP = 'TEMP', 'Temporary Access'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='auth_tokens',
        verbose_name='Utilisateur'
    )
    token = models.CharField(max_length=255, unique=True)
    token_type = models.CharField(
        max_length=10,
        choices=TokenType.choices,
        default=TokenType.API
    )
    name = models.CharField(max_length=100, help_text='Nom descriptif du token')
    scopes = models.JSONField(default=list, help_text='Liste des permissions accordées')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_from_ip = models.GenericIPAddressField()

    class Meta:
        verbose_name = 'Jeton d\'authentification'
        verbose_name_plural = 'Jetons d\'authentification'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'token_type']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.token_type}) - {self.user.username}"

    @property
    def is_expired(self):
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def revoke(self):
        self.is_active = False
        self.save()

    def update_last_used(self):
        self.last_used_at = timezone.now()
        self.save(update_fields=['last_used_at'])

class TrustedDevice(models.Model):
    """Gestion des appareils de confiance"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trusted_devices',
        verbose_name='Utilisateur'
    )
    device_id = models.CharField(max_length=255, unique=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    os_info = models.CharField(max_length=100)
    browser_info = models.CharField(max_length=100)
    last_ip = models.GenericIPAddressField()
    last_location = models.CharField(max_length=100, blank=True)
    trust_score = models.PositiveSmallIntegerField(default=0)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_trusted = models.BooleanField(default=False)
    requires_2fa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Appareil de confiance'
        verbose_name_plural = 'Appareils de confiance'
        indexes = [
            models.Index(fields=['device_id']),
            models.Index(fields=['user', 'is_trusted']),
        ]

    def __str__(self):
        return f"{self.device_name} - {self.user.username}"

    def update_trust_score(self, success=True):
        if success:
            self.trust_score = min(100, self.trust_score + 5)
        else:
            self.trust_score = max(0, self.trust_score - 10)
        self.save(update_fields=['trust_score'])

    @property
    def is_highly_trusted(self):
        return self.trust_score >= 80

class SecurityEvent(models.Model):
    """Historique des événements de sécurité"""
    class EventType(models.TextChoices):
        PASSWORD_CHANGE = 'PWD_CHANGE', 'Changement de mot de passe'
        EMAIL_CHANGE = 'EMAIL_CHANGE', 'Changement d\'email'
        LOGIN_SUCCESS = 'LOGIN_OK', 'Connexion réussie'
        LOGIN_FAILED = 'LOGIN_FAIL', 'Échec de connexion'
        LOGOUT = 'LOGOUT', 'Déconnexion'
        TOKEN_CREATED = 'TOKEN_NEW', 'Création de token'
        TOKEN_REVOKED = 'TOKEN_REVOKE', 'Révocation de token'
        DEVICE_TRUSTED = 'DEV_TRUST', 'Appareil approuvé'
        DEVICE_REMOVED = 'DEV_REMOVE', 'Appareil supprimé'
        SECURITY_CHANGE = 'SEC_CHANGE', 'Modification des paramètres de sécurité'
        SUSPICIOUS_ACTIVITY = 'SUSPICIOUS', 'Activité suspecte'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='security_events',
        verbose_name='Utilisateur'
    )
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices
    )
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    device_info = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.PositiveSmallIntegerField(
        default=0,
        help_text='0: Info, 1: Low, 2: Medium, 3: High'
    )
    related_token = models.ForeignKey(
        AuthToken,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    related_device = models.ForeignKey(
        TrustedDevice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    additional_data = models.JSONField(default=dict)

    class Meta:
        verbose_name = 'Événement de sécurité'
        verbose_name_plural = 'Événements de sécurité'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['severity']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.user.username} - {self.created_at}"

    @classmethod
    def log_event(cls, user, event_type, description, ip_address, device_info, 
                  severity=0, location='', **kwargs):
        """Crée un nouvel événement de sécurité"""
        return cls.objects.create(
            user=user,
            event_type=event_type,
            description=description,
            ip_address=ip_address,
            device_info=device_info,
            severity=severity,
            location=location,
            additional_data=kwargs
        )

    @property
    def is_high_severity(self):
        return self.severity >= 3

    def notify_user(self):
        """Envoie une notification à l'utilisateur si l'événement est important"""
        if self.severity >= 2:
            # Logique de notification à implémenter
            pass

class RevokedToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    revoked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'revoked_tokens'
        indexes = [
            models.Index(fields=['jti']),
            models.Index(fields=['user', 'revoked_at']),
        ]

    @classmethod
    def is_revoked(cls, jti):
        return cls.objects.filter(jti=jti).exists()



