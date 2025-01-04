# Generated by Django 5.0 on 2024-01-05 12:00

import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SecurityPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('require_2fa', models.BooleanField(default=False)),
                ('notify_on_login', models.BooleanField(default=True)),
                ('max_sessions', models.IntegerField(default=5)),
                ('trusted_locations', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='security_preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrustedDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255)),
                ('device_name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=50)),
                ('is_trusted', models.BooleanField(default=False)),
                ('trust_score', models.IntegerField(default=0)),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trusted_devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'device_id')},
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('device_type', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('LOGIN_SUCCESS', 'Connexion réussie'), ('LOGIN_FAILED', 'Échec de connexion'), ('LOGOUT', 'Déconnexion'), ('PASSWORD_CHANGE', 'Changement de mot de passe'), ('EMAIL_CHANGE', 'Changement d\'email'), ('DEVICE_TRUSTED', 'Appareil approuvé'), ('DEVICE_UNTRUSTED', 'Appareil révoqué'), ('SECURITY_CHANGE', 'Modification des paramètres de sécurité')], max_length=50)),
                ('description', models.TextField()),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('severity', models.IntegerField(choices=[(1, 'Faible'), (2, 'Moyen'), (3, 'Élevé')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='security_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RevokedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jti', models.CharField(max_length=255, unique=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('revoked_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revoked_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('device_type', models.CharField(max_length=50)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('login_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'Réussi'), ('FAILED', 'Échoué')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-login_time'],
            },
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('ip_address', models.GenericIPAddressField()),
                ('attempt_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('SUCCESS', 'Réussi'), ('FAILED', 'Échoué'), ('BLOCKED', 'Bloqué')], max_length=10)),
                ('user_agent', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-attempt_time'],
            },
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_verifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('token_type', models.CharField(choices=[('ACCESS', 'Access Token'), ('REFRESH', 'Refresh Token'), ('RESET', 'Reset Token'), ('VERIFY', 'Verify Token')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('device_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='securityevent',
            index=models.Index(fields=['user', '-created_at'], name='auth_securi_user_id_c4c7d4_idx'),
        ),
        migrations.AddIndex(
            model_name='loginhistory',
            index=models.Index(fields=['user', '-login_time'], name='auth_loginh_user_id_c89429_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['email', '-attempt_time'], name='auth_logina_email_d66f9c_idx'),
        ),
        migrations.AddIndex(
            model_name='loginattempt',
            index=models.Index(fields=['ip_address', '-attempt_time'], name='auth_logina_ip_addr_c00ec0_idx'),
        ),
    ]
