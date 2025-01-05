from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='User', **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        extra_fields.setdefault('role', role)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Administrator')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('User', 'Simple utilisateur'),
        ('Provider', 'Prestataire'),
        ('Administrator', 'Administrateur'),
        ('Moderator', 'Modérateur'),
        ('Staff', 'Personnel'),
    ]

    email = models.EmailField(
        unique=True,
        help_text='Email address used for authentication'
    )
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='User',
        help_text='Rôle de l\'utilisateur'
    )
    password_changed_at = models.DateTimeField(null=True, blank=True)
    security_score = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"
