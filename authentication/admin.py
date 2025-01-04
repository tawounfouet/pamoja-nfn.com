from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User,
    UserSession,
    LoginAttempt,
    LoginHistory,
    SecurityPreference,
    TrustedDevice,
    SecurityEvent,
    RevokedToken,
    EmailVerification,
    PhoneVerification,
    AuthToken
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_type', 'ip_address', 'is_active', 'created_at', 'last_activity')
    list_filter = ('is_active', 'device_type', 'created_at')
    search_fields = ('user__email', 'ip_address', 'device_type')
    ordering = ('-created_at',)

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'status', 'attempt_time')
    list_filter = ('status', 'attempt_time')
    search_fields = ('email', 'ip_address')
    ordering = ('-attempt_time',)

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'device_type', 'login_time', 'location')
    list_filter = ('login_time', 'device_type')
    search_fields = ('user__email', 'ip_address', 'location')
    ordering = ('-login_time',)

@admin.register(SecurityPreference)
class SecurityPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'require_2fa', 'notify_on_login', 'max_sessions')
    list_filter = ('require_2fa', 'notify_on_login')
    search_fields = ('user__email',)

@admin.register(TrustedDevice)
class TrustedDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'device_type', 'is_trusted', 'trust_score', 'last_seen')
    list_filter = ('is_trusted', 'device_type', 'last_seen')
    search_fields = ('user__email', 'device_name', 'device_id')
    ordering = ('-last_seen',)

@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'severity', 'created_at', 'ip_address')
    list_filter = ('event_type', 'severity', 'created_at')
    search_fields = ('user__email', 'description', 'ip_address')
    ordering = ('-created_at',)

@admin.register(RevokedToken)
class RevokedTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'jti', 'revoked_at', 'expires_at')
    list_filter = ('revoked_at', 'expires_at')
    search_fields = ('user__email', 'jti', 'reason')
    ordering = ('-revoked_at',)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_verified', 'created_at', 'verified_at')
    list_filter = ('is_verified', 'created_at', 'verified_at')
    search_fields = ('user__email', 'email')
    ordering = ('-created_at',)

@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_verified', 'created_at', 'verified_at')
    list_filter = ('is_verified', 'created_at', 'verified_at')
    search_fields = ('user__email', 'phone_number')
    ordering = ('-created_at',)

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_type', 'created_at', 'expires_at', 'is_active')
    list_filter = ('token_type', 'is_active', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)